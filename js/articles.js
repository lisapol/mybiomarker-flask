'use strict';
let article_list = document.querySelector('.article-list');
let hide = document.querySelector('.hide');

hide.onclick = function() {
  for(let i = 2; i < 4; i++) {
    if(article_list.children[i].style.display != 'none') {
      article_list.children[i].style.display = 'none';
    }
    else {
      article_list.children[i].style.display = 'grid';
      article_list.children[i].style.display = 'grid';
    }
  };
};

if(window.innerWidth <= 768) {
  for(let i = 2; i < 4; i++) {
    article_list.children[i].style.display = 'none';
  }
};
/*
window.addEventListener(`resize`, function() {
  if(window.innerWidth <= 768) {
    for(let i = 0; i < article_list.children.length; i++) {
      if(i > 1) {
        article_list.children[i].style.display = 'none';
      }
    }
  }
  else {
    for(let i = 0; i < article_list.children.length; i++) {
      if(i > 1) {
        article_list.children[i].style.display = 'block';
      }
    }
  };
});
*/
//var theForm = document.getElementById('form');
//theForm.addEventListener('submit', function(event) {
//  event.preventDefault();

var modal = null
function pop() {
   if(modal === null) {
     document.getElementById("box").style.display = "block";
     modal = true
   } else {
     document.getElementById("box").style.display = "none";
     modal = null
}}