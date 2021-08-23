from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer, Comment
from .forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
def index(request):
    """
    pybo 목록 출력
    """
    # 페이지 입력 파라미터
    page=request.GET.get('page', '1') # url 에서 page값 없이 호출되면 default page=1
    question_list=Question.objects.order_by('-create_date') 
    # create_date 역순으로 조회. - 는 역순(최신순)

    #페이징 처리
    paginator=Paginator(question_list, 10)
    page_obj=paginator.get_page(page)
    max_page=len(page_obj.paginator.page_range)
    context={'question_list': page_obj, 'max_page_num':max_page}
    # context={'question_list': question_list} #페이지 처리 전
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    # pybo 내용 출력
    #question=Question.objects.get(id=question_id)
    question=get_object_or_404(Question, pk=question_id)
    context={'question': question}
    return render(request, 'pybo/question_detail.html', context)

"""def answer_create(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id) #urls에 있는 detail 페이지 불러오기
    """

"""request.user가 로그인 user상태여야 작동한다. login_required를 사용하면 
로그인 되있지 않을때 자동으로 로그인창으로 이동
"""
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    if request.method=='POST':
        form=AnswerForm(request.POST)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.author=request.user
            answer.question=question
            answer.create_date=timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form=AnswerForm()
    
    context={'question':question, 'form':form}

    return render(request, "pybo/question_detail.html", context)

@login_required(login_url='common:login')
def question_create(request):
    if request.method=='POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question=form.save(commit=False)
            question.author=request.user
            question.create_date=timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form=QuestionForm()
    return render(request, "pybo/question_form.html", {'form':form})

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    질문수정
    """
    question=get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    if request.method=="POST":
        form=QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question=form.save(commit=False)
            question.modify_date=timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)

    else:
        form=QuestionForm(instance=question)
    context={'form':form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    질문삭제
    """
    question=get_object_or_404(Question, pk=question_id)
    if request.user !=question.author:
        messages.error(request, '삭제권한 없음')
        return redirect('pybo:detail', question_id=question.id)

    question.delete()
    return redirect('pybo:index')

@login_required(login_url="common:login")
def answer_modify(request, answer_id):
    """
    답변삭제
    """
    answer=get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method=="POST":
        form=AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.modify_date=timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form=AnswerForm(instance=answer)
    context={'answer':answer, 'form':form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url="common:login")
def answer_delete(request, answer_id):
    """
    답변삭제
    """
    answer=get_object_or_404(Answer, pk=answer_id)
    if request.user!=answer.author:
        messages.error(request, '삭제권한 없음')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)


## 질문 댓글
@login_required(login_url="common:login")
def comment_create_question(request, question_id):
    """
    질문 댓글 생성
    """
    question=get_object_or_404(Question, pk=question_id)
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user
            comment.create_date=timezone.now()
            comment.question=question
            comment.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form=CommentForm()
    context={'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url="common:login")
def comment_modify_question(request, comment_id):
    """
    질문 댓글 수정
    """
    comment=get_object_or_404(Comment, pk=comment_id)
    if request.user!=comment.author:
        messages.error(request, '댓글 수정 권한 없음')
        return redirect('pybo:detail', question_id=comment.question.id)
    
    if request.method=="POST":
        form=CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.modify_date=timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else:
        form=CommentForm(instance=comment)
    context={'form':form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url="common:login")
def comment_delete_question(request, comment_id):
    """
    질문 댓글 삭제
    """
    comment=get_object_or_404(Comment, pk=comment_id)
    if request.user!=comment.author:
        messages.error(request, '댓글 삭제 권한 없음')
        return redirect('pybo:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)


## 답변 댓글
@login_required(login_url="common:login")
def comment_create_answer(request, answer_id):
    """
    답변 댓글 생성
    """
    answer=get_object_or_404(Answer, pk=answer_id)
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user
            comment.create_date=timezone.now()
            comment.answer=answer
            comment.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form=CommentForm()
    context={'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url="common:login")
def comment_modify_answer(request, comment_id):
    """
    질문 댓글 수정
    """
    comment=get_object_or_404(Comment, pk=comment_id)
    if request.user!=comment.author:
        messages.error(request, '댓글 수정 권한 없음')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    
    if request.method=="POST":
        form=CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.modify_date=timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form=CommentForm(instance=comment)
    context={'form':form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url="common:login")
def comment_delete_answer(request, comment_id):
    """
    질문 댓글 삭제
    """
    comment=get_object_or_404(Comment, pk=comment_id)
    if request.user!=comment.author:
        messages.error(request, '댓글 삭제 권한 없음')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)