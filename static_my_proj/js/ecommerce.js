// this is made to connect to templates/base.html

$(document).ready(function(){

    console.log("readyyyy")
    // contact form habdrler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")  /* questo lo prende da dove ho scritto action nella view dei contatti */
    

    function displaySubmitting(submitBtn, defaultText, doSubmit){

      if (doSubmit){
        submitBtn.addClass("disabled")
        submitBtn.html("<i class='fa fa-span fa-spinner'></i> Sending...")
      } else {
        submitBtn.removeClass("disabled")
        submitBtn.html(defaultText)
      }

    }


    console.log("before submit")

    contactForm.submit(function(event){
      event.preventDefault()  /* quest mi serve a prevenire che lancio il submit premendo invio */
      

      var ContactFormSubmitBtn = contactForm.find("[type='submit']")
      var ContactFormSubmitBtnTxt = ContactFormSubmitBtn.text()

      console.log("entro submit")
      
      var contactFormData = contactForm.serialize()
      console.log("serializzazione ok")
      var thisForm = $(this)

      displaySubmitting(ContactFormSubmitBtn, "", true)
      
      $.ajax({

        method: contactFormMethod,
        url: contactFormEndpoint,
        data: contactFormData,

        success: function(data){
          contactForm[0].reset()  /* empty the form */
          $.alert({
            title: "success!",
            content: data.message,
            theme: "modern",
          })

          setTimeout(function(){
            displaySubmitting(ContactFormSubmitBtn, ContactFormSubmitBtnTxt, false)
          }, 500)

        }, /* success chiudo */

        error: function(error){
          console.log(error.responseJSON)
          var jsonData = error.responseJSON
          var msg = ""

          $.each(jsonData, function(key, value){
            msg += key + ": " + value[0].message + "<br/>"
          })

          $.alert({
            title: "oops",
            content: msg,
            theme: "modern",
          })

          setTimeout(function(){
            displaySubmitting(ContactFormSubmitBtn, ContactFormSubmitBtnTxt, false)
          }, 500)


        }, /* chiudo error */

      }) /* chiudo ajax  */


    }) /* chuso contactofrm submint */

    // autosearch
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']") /* questo mi permette di ottenere l'imput immesso nl form */
    var typingTimer;
    var typingInterval = 1500 // milli seconds
    var searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){  // when the key is released
      // console.log(event)
      // console.log(searchInput.val())

      clearTimeout(typingTimer) // clear timeout whenever a key comes up - altrimenti inizia a contare sempre dalla prima
      typingTimer = setTimeout(performSearch, typingInterval)

      })


    searchInput.keydown(function(event){  // when the key is down
      clearTimeout(typingTimer)
      })

    
    function displaySearch(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-span fa-spinner'></i> Autosearch...")
      }


    function performSearch(){
      displaySearch()
      var query = searchInput.val()
      setTimeout(function(){
        window.location.href='/search/?q=' + query
      }, 1000)
      
    }


    // cart + add products
    var productForm = $(".form-product-ajax")
    
    productForm.submit(function(event){
      event.preventDefault();

      // console.log("Form is not sending")
      var thisForm = $(this)
      // var actionEndpoint = thisForm.attr("action")  // api endpoint
      var actionEndpoint = thisForm.attr("action") //
      var httpMethod = thisForm.attr("method");
      var formData = thisForm.serialize();

      console.log(thisForm.attr("action"), thisForm.attr("method"))

      // instead of running a simple sincronous request, we run an asinchronous via ajax
      $.ajax({
          url: actionEndpoint,  
          // usiamo un action endpoint e non un api endpoint perhcè vogliamo essere sicuri che il sito funziona anche se l'utente disabilita javascript
          method: httpMethod,
          data: formData,
          success: function(data){
            console.log("yay!")
            console.log(data)
            console.log("added: ", data.added)
            console.log("removed: ", data.removed)
            var submitSpan = thisForm.find(".submit-span")
            if (data.added){
              submitSpan.html("In cart<button type='submit' class='btn btn-link'>Remove</button>") 
              // console.log(submitSpan.html())
            } else {
              submitSpan.html("<button class='btn btn-success' type='submit'>Add to Cart</button>")
              // console.log(submitSpan.html())
            }                
            
            var navbarCount = $(".navbar-cart-count")
            navbarCount.text(data.cartItemCount)
            var currentPath = window.location.href

            if (currentPath.indexOf("cart") != -1) {
              refreshCart()
            }
          },
          error: function(errorData){
            // dollar sign davanti ad alert serve ad attivare jquery-confirm
            // alert("an error occurred!!")
            // $.alert("an error occurred!!")
            $.alert({
              title: "Error!",
              content: "an error occurred!!",
              theme: "modern",
            })

            console.log("error")
            console.log(errorData)
          }

      })

    })

    function refreshCart(){
      console.log("in current cart")
      var cartTable = $(".cart-table")
      var cartBody = cartTable.find(".cart-body")
      // cartBody.html("<h1>Changed</h1>")

      var productRows = cartBody.find(".cart-product")
      var currentUrl = window.location.href


      var refreshCartUrl = '/api/cart/';
      var refreshCartMethod = "GET";
      var data = {};

      $.ajax({
        url: refreshCartUrl,
        method: refreshCartMethod,
        data: data,
        success: function(data){

          var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
          // console.log("success refreshCart")
          // console.log(data)

          if (data.products.length > 0){
            // productRows.html("<tr><td colspan=3>Coming Soon</td></tr>")
            productRows.html(" ")
            i = data.products.length
            $.each(data.products, function(index, value){
              console.log(value)
              var newCartItemRemove = hiddenCartItemRemoveForm.clone()
              newCartItemRemove.css("display", "block")
              // hiddenCartItemRemoveForm.removeClass("hidden-class")
              newCartItemRemove.find(".cart-item-product-id").val(value.id)

              cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
          })
            i--
            cartBody.find(".cart-subtotal").text(data.subtotal)
            cartBody.find(".cart-total").text(data.total)
          } else {
            window.location.href = currentUrl
          }

        },
        error: function(errorData){

          // i can place it everywhere I have an error of ajax
          $.alert({
              title: "Error!",
              content: "an error occurred!!",
              theme: "modern",
            })

          console.log("error refreshCart")
          console.log(errorData)
        },

      })

    }


  })