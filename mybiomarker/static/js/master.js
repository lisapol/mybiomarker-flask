'use strict'
let control = document.querySelectorAll('.control');
let question_answer = document.querySelectorAll('.question-answer');
let mobile_btn = document.querySelector('.mobile-btn');
let close = document.querySelector('.close');
let mobile_menu = document.querySelector('.mobile-menu');

let file_input = document.querySelector('#file-input');
let file_add = document.querySelector('.file-add');

file_input.onclick = function() {
  file_add.textContent = file_input.value;
};

let question_title = document.querySelectorAll('.question-title');


/*
for(let i = 0; i < control.length; i++) {
  console.log(control[i]);
  control[i].children[1].style.display = 'none';
  question_answer[i].style.height = 0;
  control[i].children[0].onclick = function() {
    control[i].children[1].style.display = 'block';
    control[i].children[0].style.display = 'none';
    question_answer[i].style.height = 'auto';
    control[i].children[1].onclick = function() {
      control[i].children[0].style.display = 'block';
      control[i].children[1].style.display = 'none';
      question_answer[i].style.height = 0;
    };
  };
};
*/

mobile_btn.onclick = function() {
  mobile_menu.style.display = 'block';
  close.onclick = function() {
    mobile_menu.style.display = 'none';
  };
};


for(let b = 0; b < question_title.length; b++) {
  control[b].children[1].style.display = 'none';
  question_answer[b].style.height = 0;
  question_title[b].onclick = function() {
    if(question_answer[b].style.height != 'auto') {
      question_answer[b].style.height = 'auto';
      control[b].children[1].style.display = 'block';
      control[b].children[0].style.display = 'none';
    }
    else {
      question_answer[b].style.height = 0;
      control[b].children[1].style.display = 'none';
      control[b].children[0].style.display = 'block';
    }
  };
};

$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
//				name : $('#nameInput').val(),
				email : $('#form-input').val()
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).fadeIn().fadeOut(3500);
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.name).fadeIn().fadeOut(3500);
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});

const cookieStorage = {
    getItem: (item) => {
        const cookies = document.cookie
            .split(';')
            .map(cookie => cookie.split('='))
            .reduce((acc, [key, value]) => ({ ...acc, [key.trim()]: value }), {});
        return cookies[item];
    },
    setItem: (item, value) => {
        document.cookie = `${item}=${value};`
    }
}

const storageType = cookieStorage;
const consentPropertyName = 'jdc_consent';
const shouldShowPopup = () => !storageType.getItem(consentPropertyName);
const saveToStorage = () => storageType.setItem(consentPropertyName, true);

//window.onload = () => {
//
//    const acceptFn = event => {
//        saveToStorage(storageType);
//        consentPopup.classList.add('hidden');
//    }
//
//    const consentPopup = document.getElementById('consent-popup');
//    const acceptBtn = document.getElementById('accept');
//    acceptBtn.addEventListener('click', acceptFn);
//    console.log(shouldShowPopup(storageType));
//
//    if (shouldShowPopup(storageType)) {
//        setTimeout(() => {
////            consentPopup.classList.remove('hidden');
//        document.getElementById('consent-popup').style.display = "none";
//        }, 200);
//    }
//
//};

$( "#accept" ).click(function() {
  $( "#consent-popup" ).fadeOut( "fast", function() {
    // Animation complete.
  });
});