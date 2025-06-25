from django.shortcuts import render, redirect, Http404
from .models import ReviewManager, TrainingProgramManager

def reviews_list(request):
    reviews = ReviewManager.get_random_reviews()
    return render(request, 'review_list.html', {'reviews': reviews})

def program_list(request):
    programs = TrainingProgramManager.get_all_programs()
    return render(request, 'program_list.html', {
        'training_programs': programs
    })

def program_detail(request, id):
    program = TrainingProgramManager.get_program_with_averages(id)
    if not program:
        raise Http404("指定された研修が見つかりません")
    
    # クエリパラメータから認証状態を取得（デフォルトは False）
    auth_param = request.GET.get("auth", "").lower()
    is_authenticated = auth_param == "true"

    industry_id_param = request.GET.get("industry_id", "0")
    try:
        industry_id = int(industry_id_param)
    except ValueError:
        industry_id = 0

    # industoriesテーブルから一覧取得
    industories = TrainingProgramManager.get_all_industories()
    
    # レビュー取得（業種フィルタ有無）
    reviews = v.get_reviews_for_program(
        program_id=id,
        industory_id=industry_id,
        limit=10
    )

    return render(request, 'program_detail.html', {
        'program': program,
        'reviews': reviews,
        'is_authenticated': is_authenticated,
        'industories': industories,
        'selected_industry_id': industry_id
    })

