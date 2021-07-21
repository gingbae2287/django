from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question,Choice
# from django.template import loader
# from django.http import Http404

# 제너릭 뷰 사용-> 코드적고 간편
class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model=Question
    template_name='polls/detail.html'

class ResultsView(generic.DetailView):
    model=Question
    template_name='polls/results.html'



def index(request):
    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    #template=loader.get_template("polls/index.html")
    context={'latest_question_list': latest_question_list,}
    # return HttpResponse(template.render(context,request)) # or
    return render(request, 'polls/index.html',context)

    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

def detail(request, question_id):
    # try:
    #     question=Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("질문읎다")
    # return render(request, 'polls/detail.html', {'question':question})
    # 위 코드는 자주 쓰이는 방식이라 아래와 같이 구현돼있다. get_object_or_404() 또는 get_list_or_404() list는 get 대신 filter 쓴다
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html', {'question':question})

    # return HttpResponse("You're looking at question %s." %question_id)

def results(request, question_id):
    question=get_object_or_404(Question,pk=question_id)
    # response="You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question': question,
            'error_message': "선택하세요",
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))