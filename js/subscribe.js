var submitted = false;

window.addEventListener('load', function() {
    // Get all forms and message divs
    var forms = document.getElementsByTagName('form');
    var messages = document.querySelectorAll('#subscribeMessage');
    
    // Handle iframe load event
    var iframe = document.getElementById('hidden_iframe');
    if (iframe) {
        iframe.addEventListener('load', function() {
            if (submitted) {
                // Show success message
                messages.forEach(function(message) {
                    message.style.display = 'block';
                    setTimeout(function() {
                        message.style.display = 'none';
                    }, 5000);
                });
                
                // Reset forms
                for (var i = 0; i < forms.length; i++) {
                    forms[i].reset();
                }
                
                submitted = false;
            }
        });
    }
    
    // Add submit handler to forms
    for (var i = 0; i < forms.length; i++) {
        forms[i].addEventListener('submit', function() {
            submitted = true;
            var button = this.querySelector('button[type="submit"]');
            if (button) {
                button.disabled = true;
                button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Subscribing...';
                setTimeout(function() {
                    button.disabled = false;
                    button.innerHTML = 'Notify Me';
                }, 2000);
            }
        });
    }
});
