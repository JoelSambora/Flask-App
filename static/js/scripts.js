/*!
* Start Bootstrap - Creative v7.0.6 (https://startbootstrap.com/theme/creative)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList;
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent;

var recognition = new SpeechRecognition();
var speechRecognitionList = new SpeechGrammarList();
recognition.lang = 'en-GB';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

const button = document.getElementById("start");
const input = document.getElementById("search");
const supportmsg = document.getElementById("support-msg");

if ('SpeechRecognition' in window) {
  button.classList.add("supported");
  supportmsg.classList.add("supported");
}

button.addEventListener("click", function(){
  recognition.start();
  button.innerHTML = "Listening...";
  button.classList.add("glow");
  console.log('Ready to receive voice input.');
});

recognition.onresult = function(event) {
  var last = event.results.length - 1;
  var searchResult = event.results[last][0].transcript;
  button.innerHTML = "Click to speak";
  input.value = searchResult;
  button.classList.remove("glow");
  console.log(searchResult);
}

recognition.onspeechend = function() {
  recognition.stop();
}

recognition.onnomatch = function(event) {
  console.log('Not recognised');
  button.innerHTML = "Click to speak";
}

recognition.onerror = function(event) {
  console.log('Error occurred in recognition: ' + event.error);
  button.innerHTML = "Click to speak";
}

