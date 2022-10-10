const nav = document.querySelector('nav');
const dark = window.matchMedia("(max-width: 992px)");
const nav_button = document.getElementById('nav_button')


window.addEventListener('scroll', function(){
  if(window.scrollY > 100){
    nav.classList.add('bg-dark', 'shadow')
  }else{
    nav.classList.remove('bg-dark', 'shadow')

  }
});


function reveal() {
  var reveals = document.querySelectorAll(".reveal");

  for (var i = 0; i < reveals.length; i++) {
      var windowHeight = window.innerHeight;
      var elementTop = reveals[i].getBoundingClientRect().top;
      var elementVisible = 20;

      if (elementTop < windowHeight - elementVisible) {
          reveals[i].classList.add("active");
      } else {
          reveals[i].classList.remove("active");
      }
  }
}

function reveal_once() {
  var reveals = document.querySelectorAll(".reveal_once");

  for (var i = 0; i < reveals.length; i++) {
      var windowHeight = window.innerHeight;
      var elementTop = reveals[i].getBoundingClientRect().top;
      var elementVisible = 20;

      if (elementTop < windowHeight - elementVisible) {
          reveals[i].classList.add("active");
      }
  }
}


window.addEventListener("scroll", reveal);
window.addEventListener("scroll", reveal_once);
                 


setTimeout(function() {
  bootstrap.Alert.getOrCreateInstance(document.querySelector(".alert")).close();
}, 3000)


var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

