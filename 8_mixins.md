# Миксины в Python


В Python нет специального синтаксиса, предназначенного для выделения миксинов из множества классов. На самом деле, достаточно обычного класса с припиской `Mixin`, чтобы все всё поняли.


Использовать миксины следует тогда, когда требуется внести дополнительную функциональность в существующую иерархию наследования, но нельзя менять существующущий код или, по крайней мере, не везде такая функциональность требуется.


Пример использования можно обнаружить в фреймворке Django. Класс `TemplateView` позвоялет произвести рендер шаблона лишь в ответ на запрос GET, но что делать в случае, если требуется рендерить шаблон и в ответ на PUT?

``` python
class MyView(TemplateView):
    template_name = 'my_template.html'
```

Можно было бы унаследоваться от `View` и реализовать вручную два метода, но это приводит к дублированию кода.

``` python
class MyView(View):
    def post(self, request, *args, **kwargs):
        return TemplateResponse(
            request=request,
            template='my_template.html'
        )

    def put(self, request, *args, **kwargs):
        return TemplateResponse(
            request=request,
            template='my_template.html'
        )
```

Django предлагает готовое средство - TemplateResponseMixin, миксин, предоставляющий функциональность по рендеру шаблонов. Применяя его посредством множественного наследования возможно избежать излишнего дублирования кода:

``` python
class MyView(TemplateResponseMixin, View):

    template_name = 'my_template.html'

    def post(self, request, *args, **kwargs):
        return self.render_to_response(context={})

    def put(self, request, *args, **kwargs):
        return self.render_to_response(context={})
```

Django предусматривает и миксин `ContextMixin` для добавления в класс функциональности по получению переменных контекста.

``` python
class MyView(TemplateResponseMixin, ContextMixin, View):

    template_name = 'my_template.html'

    def post(self, request, *args, **kwargs):
        return self.render_to_response(context=self.get_context_data())

    def put(self, request, *args, **kwargs):
        return self.render_to_response(context=self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your context variables here
        return context
```
