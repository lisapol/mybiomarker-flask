'use strict'
let mobile_btn = document.querySelector('.mobile-btn');
let close = document.querySelector('.close');
let mobile_menu = document.querySelector('.mobile-menu');


mobile_btn.onclick = function() {
  mobile_menu.style.display = 'block';
  close.onclick = function() {
    mobile_menu.style.display = 'none';
  };
};


