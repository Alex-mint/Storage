const appVue = Vue.createApp({
    data() {


        
        return {
            cart: 1,
            test: 15,
            total: 15,
            product: 'Socks',
            brend: 'Adidas',
            image: './assets/images/socks_green.jpg',
            inStock: true,
            inventory: 100,
            details: ['cotton 80%', 'wool 20%'],
            variants: [
                {id: 2233, color: 'green', image: './assets/images/socks_green.jpg'},
                {id: 2234, color: 'blue', image: './assets/images/socks_blue.jpg'},
            ]
        }
    },

    methods: {
        addToCart() {
            this.cart += 1
            this.total += this.price 
            this.inventory -= 1
        },
        removeFromCart() {
            this.cart -= 1 
            this.total -= this.price
            this.inventory += 1
        },
        updateImage(updateImage) {
            this.image = updateImage
        }
    },

    computed: {
        title() {
            return this.brend + ' ' + this.product
        }
    }

  
})

appVue.config.compilerOptions.delimiters = [ '[[', ']]' ]
const mountedApp = app.mount('#vue')