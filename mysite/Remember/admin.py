from django.contrib import admin

from .models import Patient, Reminder, User, PatientClearanceAbstraction, Quiz, Question, QuizResult, QuestionResult

# Register your models here.

admin.site.register(Patient)
admin.site.register(Reminder)
admin.site.register(User)
admin.site.register(PatientClearanceAbstraction)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizResult)
admin.site.register(QuestionResult)


'''
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_filter = ['pub_date']
    search_fields = ['question_text']
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')

admin.site.register(Question, QuestionAdmin)

'''


# simular to the code above, but this allows us to change order of the feild in the admin site.
#admin.site.register(Choice)