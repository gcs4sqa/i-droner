import os
import PySimpleGUI as sg


def getImages():
    responecode = os.system("timeout 10s kubectl get pod 1> /dev/null")

    # show popup window if no VPN is active
    if responecode != 0:
        window = sg.Window
        sg.Popup('You do not have a VPN connection active', 'Please activate your VPN to Kubernetes', no_titlebar=True)
        window.close

    # delete all completed jobs
    os.system(
        "kubectl delete job -n gap-st $(kubectl get job -n gap-st -o=jsonpath='{.items[?(@.status.succeeded==1)].metadata.name}')")

    # grab all current images from gap-st
    images = os.popen(
        'kubectl get pods -n gap-st -o jsonpath=\"{.items[*].spec.containers[*].image}\" | tr -s \'[[:space:]]\' \'\n\' | sort'
        ' |uniq -c | sed \'/automation/d\' | sed \'/mock/d\' | cut -d "/" -f3 | sed \':a;N;$!ba;s/\\n/,/g\'')

    return images.read()
