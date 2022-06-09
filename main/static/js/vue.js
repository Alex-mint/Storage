let CartVue = JSON.parse(document.getElementById('cart_vue').textContent);

const appVue = Vue.createApp({
    
    data() {


        
        return {
            month: CartVue.month,
            subTotal: 0,
            total: CartVue.total,
            items: CartVue.items,
        }
    },

    methods: {
        addMonth() {
            this.subTotal = 0
            this.month += 1 
        },
        lessMonth() {
            this.subTotal = 0
            this.month -= 1
        },
        addItem(itemId) {
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
            this.subTotal = 0
            for (var i = 0; i < this.items.length; i++) {
                var item = this.items[i];

                if (item.id === itemId) {
                    item.qty -= 1
                    item.final_price = item.qty * item.price
                }
            }
            
        }
        
    },

    computed: {
        
        title() {
            for (let i = 0; i < this.items.length; i++) {
                this.subTotal += Number(this.items[i].final_price)
                console.log('subT: ' + this.subTotal)
                console.log('FinP: ' + this.items[i].final_price)
                
             }
            console.log('Final: ' + this.month * this.subTotal)
            return this.month * this.subTotal
        }
    }

  
})

appVue.config.compilerOptions.delimiters = [ '[[', ']]' ]
const mountedApp = appVue.mount('#vue')