const nav = document.querySelector('nav');
const dark = window.matchMedia("(max-width: 992px)");
const nav_button = document.getElementById('nav_button')

dark.addEventListener("change", (e) => {
  dark.onchange = (e) => {
    if (e.matches) {
      nav.classList.add('bg-dark', 'shadow')
      nav_button.onclick = function(e){
        if(e.target.id !== 'nav_button'){
          nav.classList.add('bg-dark', 'shadow')
        } else {
          nav.classList.remove('bg-dark', 'shadow')
        }
      }
    }else{
      window.addEventListener('scroll', function(){
        if(window.scrollY > 100){
          nav.classList.add('bg-dark', 'shadow')
        }else{
          nav.classList.remove('bg-dark', 'shadow')

        }
      });
    }
  };
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



// $("#success-alert").fadeTo(2000, 500).slideUp(300, function(){
//   $("#success-alert").slideUp(300);
// });
