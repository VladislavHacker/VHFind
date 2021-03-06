let signupModule = new Module({
  template: './templates/sign_up.html',
  model: {
    name: '',
    last_name: '',
    age: '',
    email: '',
    password: '',
    ckPassword: '',
    check: ''
  },
  handlers: {
    regButton: function(model) {
      if (model.name == '') {
        model.check = 'Введите имя'
        return
      }
      if (model.last_name == '') {
        model.check = 'Введите фамилию'
        return
      }
      if (model.age == '') {
        model.check = 'Введите возраст'
        return
      }
      if (model.ckPassword != model.password) {
        model.check = 'Пароли не совпадают'
        return
      }
      VHrequest({
        method: 'POST',
        url: SERVER + '/sign/up',
        data: {
          name: model.name,
          last_name: model.last_name,
          email: model.email,
          age: model.age,
          password: model.password
        }
      }).then((response) => {
        
      })
    }
  }
})
