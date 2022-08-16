const nav = document.querySelector('nav');
const dark = window.matchMedia("(max-width: 992px)");

dark.onchange = (e) => {
  if (e.matches) {
    nav.classList.add('bg-dark', 'shadow')
  }else{
    nav.classList.remove('bg-dark', 'shadow')
  }
};

dark.addEventListener("change", () => {
});


window.addEventListener('scroll', function(){
  if(window.scrollY > 100){
    nav.classList.add('bg-dark', 'shadow')
  }else{
    nav.classList.remove('bg-dark', 'shadow')
  }
});


// $("#success-alert").fadeTo(2000, 500).slideUp(300, function(){
//   $("#success-alert").slideUp(300);
// });
