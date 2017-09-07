def updateModelFromFormPost(model_instance, FormClass, request):
  if not request.method == 'POST':
    return
  form_is_complete = False
  form = FormClass(request.POST, request.FILES)
  if form.is_valid():
    form_is_complete = True
    model_instance.updateFromValidForm(form)
  return form_is_complete, form

def modelFromFormPost(ModelClass, FormClass, request):
  if not request.method == 'POST':
    return
  new_model_instance = None
  form_is_complete = False
  form = FormClass(request.POST, request.FILES)
  if form.is_valid():
    form_is_complete = True
    new_model_instance = ModelClass.fromValidForm(form)
  return new_model_instance, form_is_complete, form
