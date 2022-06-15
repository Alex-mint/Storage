axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = "csrftoken"

let CartVue = JSON.parse(document.getElementById('cart_vue').textContent);
console.log(CartVue)

const appVue = Vue.createApp({
    
    data() {
        return {
            month: CartVue.month,
            subTotal: 0,
            total: CartVue.total,
            items: CartVue.items,
            number: 0,
            tweenedNumber: 0
        }
    },

    methods: {
        addMonth() {
            this.subTotal = 0
            this.month += 1 
            this.number += 1
            axios.post(`/en/${this.month}/car-month-qty/`)
        },
        lessMonth() {
            this.subTotal = 0
            this.month -= 1
            axios.post(`/en/${this.month}/car-month-qty/`)
        },
        addItem(itemId) {
            axios.post(`/en/${itemId}/car-item/increase-qty/`)

            this.subTotal = 0
            console.log(this.items)
            for (let item of this.items) {
                
                if (item.id === itemId) {
                    item.qty += 1
                    item.final_price = Number(item.price) + Number(item.final_price)
                }
            }
            
        },
        lessItem(itemId, itemQty, itemPrice) {
            axios.post(`/en/${itemId}/car-item/reduce-qty/`)

            this.subTotal = 0
            for (var i = 0; i < this.items.length; i++) {
                var item = this.items[i];

                if (item.id === itemId) {
                    item.qty -= 1
                    item.final_price = item.qty * item.price
                }
            }
            
        },
        removeItem(item_id) {
            console.log('item_id '+ item_id)

            axios.post(`/en/${item_id}/car-item/delete/`)

            this.subTotal = 0
            for (var i = 0; i < this.items.length; i++) {
                //var data = {
                //    'item_id': item_id
                //}
                let item = this.items[i];

                if (item.id === item_id) {
                    this.items = this.items.filter(item => item.id !== item_id)
                }
            }
            console.log(this.items)
        }
        
    },

    computed: {
        
        cartPrice() {
            for (let i = 0; i < this.items.length; i++) {
                this.subTotal += Number(this.items[i].final_price)
                
             }
            
            return (this.month * this.subTotal).toFixed(0)
        },

        animatedNumber() {
            return this.tweenedNumber.toFixed(0)
          }
        },

    watch: {
          number(newValue) {
            gsap.to(this.$data, { duration: 0.5, tweenedNumber: newValue })
          }
        }
    

  
})

appVue.config.compilerOptions.delimiters = [ '[[', ']]' ]
const mountedApp = appVue.mount('#vue')