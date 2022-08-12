const nav = document.querySelector('nav')

window.addEventListener('scroll', function(){
  if(window.scrollY > 100){
    nav.classList.add('bg-dark', 'shadow')
  }else{
    nav.classList.remove('bg-dark', 'shadow')
  }
});

$("#success-alert").fadeTo(2000, 500).slideUp(500, function(){
  $("#success-alert").slideUp(500);
});
