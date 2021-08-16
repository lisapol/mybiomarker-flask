'use strict'
let control = document.querySelectorAll('.control');
let question_answer = document.querySelectorAll('.question-answer');
let mobile_btn = document.querySelector('.mobile-btn');
let close = document.querySelector('.close');
let mobile_menu = document.querySelector('.mobile-menu');


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


mobile_btn.onclick = function() {
  mobile_menu.style.display = 'block';
  close.onclick = function() {
    mobile_menu.style.display = 'none';
  };
};
