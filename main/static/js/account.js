axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = "csrftoken"

let Customer = JSON.parse(document.getElementById('customer_vue').textContent);
console.log(Customer)
const customerVue = Vue.createApp({
    
    data() {
        return {
            customer: Customer,
            city: Customer.city,
            street: Customer.street,
            number: Customer.number,
            userName: Customer.user_name,
            phone: Customer.phone,
            email: Customer.email,
        }
    },

    methods: {
        onSubmitAddress (event) {
            event.preventDefault()
            this.city = this.customer.city
            this.street = this.customer.street
            this.number = this.customer.number
            
            let bodyFormData = new FormData()
            
            bodyFormData.append('city', this.city)
            bodyFormData.append('street', this.street)
            bodyFormData.append('number', this.number)
            console.log(bodyFormData)

            axios.post('/en/edit-address/', bodyFormData)
        },

        onSubmitAccount (event) {
            event.preventDefault()
            this.first_name = this.customer.first_name
            this.last_name = this.customer.last_name
            this.phone = this.customer.phone
            this.email = this.customer.email
            
            let bodyFormData = new FormData()
            
            bodyFormData.append('first_name', this.first_name)
            bodyFormData.append('last_name', this.last_name)
            bodyFormData.append('phone', this.phone)
            bodyFormData.append('email', this.email)
            console.log(bodyFormData)

            axios.post('/en/edit-account/', bodyFormData)
        }
    }

   
    

  
})

customerVue.config.compilerOptions.delimiters = [ '[[', ']]' ]
const mountedApp = customerVue.mount('#customer')