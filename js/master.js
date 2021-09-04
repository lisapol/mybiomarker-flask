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
