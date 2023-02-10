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

document.getElementById('buttonid').addEventListener('click', openDialog);

function openDialog() {
  document.getElementById('fileid').click();
}

