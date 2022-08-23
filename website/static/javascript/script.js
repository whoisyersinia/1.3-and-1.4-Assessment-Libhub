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
      nav.classList.remvove('bg-dark', 'shadow')
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



setTimeout(function() {
  bootstrap.Alert.getOrCreateInstance(document.querySelector(".alert")).close();
}, 3000)


var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

// (function () {
//   'use strict'

//   var forms = document.querySelectorAll('.needs-validation')

//   Array.prototype.slice.call(forms)
//     .forEach(function (form) {
//       form.addEventListener('submit', function (event) {
//         if (!form.checkValidity()) {
//           event.preventDefault()
//           event.stopPropagation()
//         }

//         form.classList.add('was-validated')
//       }, false)
//     })
// })()

// function isValidISBN(isbn)
// {
       
//     // length must be 10
//     let n = isbn.length;
//     if (n != 10)
//         return false;

//     // Computing weighted sum of
//     // first 9 digits
//     let sum = 0;
//     for (let i = 0; i < 9; i++)
//     {
//         let digit = isbn[i] - '0';
           
//         if (0 > digit || 9 < digit)
//             return false;
               
//         sum += (digit * (10 - i));
//     }

//     // Checking last digit.
//     let last = isbn[9];
//     if (last != 'X' && (last < '0' || last > '9'))
//         return false;

//     // If last digit is 'X', add 10
//     // to sum, else add its value.
//     sum += ((last == 'X') ? 10 : (last - '0'));

//     // Return true if weighted sum
//     // of digits is divisible by 11.
//     return (sum % 11 == 0);
// }
 
// let isbn = "007462542X";
       
// if (isValidISBN(isbn))
//   document.write("Valid");
// else
//   document.write("Invalid");
     