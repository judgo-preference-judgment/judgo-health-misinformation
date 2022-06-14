
from braces.views import LoginRequiredMixin

from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from judgment.models import Judgment
from user.models import User
from interfaces import pref
from .models import Question, Inquiry
from response.models import Document


class InquiryView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'inquiry.html'

    def get_context_data(self, **kwargs):
        context = super(InquiryView, self).get_context_data(**kwargs)
        context["questions"] = Question.objects.all()

        return context

    def get(self, request, *args, **kwargs):
        return super(InquiryView, self).get(self, request, *args, **kwargs)


    def post(self, request, *args, **kwargs):

        if "selected_question" in self.request.POST: 

            question = Question.objects.get(
                    question_id=self.request.POST["selected_question"].strip()
            )
            inquiry, created = Inquiry.objects.get_or_create(
                    question=question, 
                    session=self.request.user.active_session
            )

            prev_judge = None
            try:
                prev_judge = Judgment.objects.filter(
                        user = self.request.user.id,
                        session=self.request.user.active_session.id,
                        inquiry=inquiry.id
                ).order_by('id').latest('id')
                state = prev_judge.after_state
            except Exception as e:
                print(f" There is no previous judgment for this question and user")
                state = pref.create_new_pref_obj(question)


            if not prev_judge or not prev_judge.is_complete:

                judgement = Judgment.objects.create(
                        user=self.request.user,
                        session= self.request.user.active_session,
                        inquiry=inquiry,
                        before_state=state,
                        parent=prev_judge,
                    )

                user = User.objects.get(id=self.request.user.id)
                user.latest_judgment = judgement
                user.save()

                return HttpResponseRedirect(
                        reverse_lazy(
                            'judgment:judgment', 
                            kwargs = {"user_id" : user.id, "judgment_id": judgement.id}
                        )
                    )
            else:
                return HttpResponseRedirect(
                        reverse_lazy(
                            'inquiry:inquiry_complete', 
                            kwargs = {"user_id" : self.request.user.id, "inquiry_id": prev_judge.inquiry.id}
                        )
                    ) 


        return HttpResponseRedirect(
                    reverse_lazy(
                        'inquiry:inquiry', 
                        kwargs = {"user_id" : self.request.user.id, 
                        "session_id": self.request.user.active_session.id}
                    )
                )




class BestAnswersView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'best_answer.html'

    def get_context_data(self, **kwargs):
        context = super(BestAnswersView, self).get_context_data(**kwargs)

        prev_judge = Judgment.objects.get(id=self.kwargs['judgment_id'])
        context['question_content'] = prev_judge.inquiry.question.content
        answer_list = prev_judge.inquiry.best_answers.split('|')[:-1]
        documets = []
        for answer in answer_list:
            documets.append(Document.objects.get(uuid=answer))
        context['documents'] = documets
        return context


    def get(self, request, *args, **kwargs):
        return super(BestAnswersView, self).get(self, request, *args, **kwargs)


    def post(self, request, *args, **kwargs):

        user = User.objects.get(id=request.user.id)
        prev_judge = user.latest_judgment

        if 'no' in request.POST:
            return HttpResponseRedirect(reverse_lazy('core:home'))

        elif 'prev' in request.POST: 
            judgement = user.latest_judgment

        if 'yes' in request.POST:
            judgement = Judgment.objects.create(
                    user=user,
                    session = user.active_session,
                    inquiry=prev_judge.inquiry,
                    before_state=prev_judge.after_state,
                    parent=prev_judge
                )
            user.latest_judgment = judgement
            user.save()
        return HttpResponseRedirect(
                reverse_lazy(
                    'judgment:judgment', 
                    kwargs = {"user_id" : user.id, "judgment_id": judgement.id}
                )
        ) 



class InquiryCompleteView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'inquiry_complete.html'

    def get_context_data(self, **kwargs):
        context = super(InquiryCompleteView, self).get_context_data(**kwargs)

        inquiry = Inquiry.objects.get(id=self.kwargs['inquiry_id'])
        context['question_content'] = inquiry.question.content
        answer_list = inquiry.best_answers.split('|')[:-1]
        documets = []
        for answer in answer_list:
            documets.append(Document.objects.get(uuid=answer))
        context['documents'] = documets
        return context


    def get(self, request, *args, **kwargs):
        return super(InquiryCompleteView, self).get(self, request, *args, **kwargs)


    def post(self, request, *args, **kwargs):

        return HttpResponseRedirect(
                reverse_lazy(
                    'core:home', 
                )
        ) 