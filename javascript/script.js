// based on https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/v1.6.0/script.js

function gradioApp() {
    const elems = document.getElementsByTagName('gradio-app');
    const elem = elems.length == 0 ? document : elems[0];

    if (elem !== document) {
        elem.getElementById = function(id) {
            return document.getElementById(id);
        };
    }
    return elem.shadowRoot ? elem.shadowRoot : elem;
}

document.addEventListener('keydown', function(e) {
    var handled = false;
    if (e.key !== undefined) {
        if ((e.key == "Enter" && (e.metaKey || e.ctrlKey || e.altKey))) handled = true;
    } else if (e.keyCode !== undefined) {
        if ((e.keyCode == 13 && (e.metaKey || e.ctrlKey || e.altKey))) handled = true;
    }
    if (handled) {
        var button = gradioApp().querySelector('button[id=generate_button]');
        if (button) {
            button.click();
        }
        e.preventDefault();
    }
});


// [TST] 2023-09-05 19:33:13
document.addEventListener("DOMContentLoaded", function() {
    var mutationObserver = new MutationObserver(function(m) {
		// play notification sound if available
		gradioApp().querySelector('#audio_notification audio')?.play();
	});
    mutationObserver.observe( gradioApp(), { childList:true, subtree:true })
}
