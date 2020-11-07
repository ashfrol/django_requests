from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся

counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_landing = request.GET.get('from-landing')
    if from_landing == 'test':
        counter_click['test'] += 1
    elif from_landing == 'original':
        counter_click['original'] += 1
    # print(counter_click['original'])
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    ab_type = request.GET.get('ab_test_arg', 'original')
    if ab_type == 'test':
        template = 'landing_alternate.html'
        counter_show['test'] += 1
    else:
        template = 'landing.html'
        counter_show['original'] += 1
    # print(counter_show['original'])
    return render(request, template)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    # print(counter_show['original'])
    # print(counter_click['original'])
    if counter_show['test'] > 0:
        test_conversion = round(int(counter_click['test'])/int(counter_show['test']), 1)
    else:
        test_conversion = 0
    # print(test_conversion)
    if counter_show['original'] > 0:
        original_conversion = round(int(counter_click['original'])/int(counter_show['original']), 1)
    else:
        original_conversion = 0
    # print(original_conversion)
    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
