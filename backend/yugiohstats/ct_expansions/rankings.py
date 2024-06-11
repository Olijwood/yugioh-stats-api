from datetime import date, timedelta
from dateutil import relativedelta

from .models import ExpSimulatedPriceStats, ExpRankings

def calculate_change(today_value, past_value):
    if past_value is not None:
        change = today_value - past_value
        change_percent = round((change / past_value) * 100, 2) if past_value != 0 else float(0)
        return change_percent
    else:
        return None

def save_cgv_rankings():
    today = date.today()
    days_7_ago = today - timedelta(days=7)
    m1_ago = today - relativedelta.relativedelta(months=1)

    stats_today = ExpSimulatedPriceStats.objects.filter(date_simulated=today).order_by('-cgv')
    stats_7d_ago =  ExpSimulatedPriceStats.objects.filter(date_simulated=days_7_ago).order_by('-cgv')
    stats_1m_ago =  ExpSimulatedPriceStats.objects.filter(date_simulated=m1_ago).order_by('-cgv')

    stats_7d_ago_dict = {stat.expansion.code: stat.cgv for stat in stats_7d_ago}
    stats_1m_ago_dict = {stat.expansion.code: stat.cgv for stat in stats_1m_ago}
    ranking = 1
    for stats in stats_today:
        exp_code = stats.expansion.code
        if stats.cgv != None:
            today_chance = round(stats.cgv, 2)
            
            # Calculate the 7-day change
            chance_7d_ago = stats_7d_ago_dict.get(exp_code)
            change_7d_percent = calculate_change(today_chance, chance_7d_ago)
            
            # Calculate the 1-month change
            chance_1m_ago = stats_1m_ago_dict.get(exp_code)
            change_1m_percent = calculate_change(today_chance, chance_1m_ago)
            
            # Calculate the all-time change
            first_cgv = ExpSimulatedPriceStats.objects.values_list('cgv', flat=True).filter(expansion__code=exp_code).order_by('date_simulated').first()
            change_all_time_percent = calculate_change(today_chance, first_cgv)

            ExpRankings.objects.update_or_create(
                expansion = stats.expansion,
                ranking_date = today,
                defaults = {
                    'cgv_ranking': ranking,
                    'cgv_today': today_chance,
                    'cgv_week': change_7d_percent,
                    'cgv_month': change_1m_percent,
                    'cgv_all_time': change_all_time_percent,
                }
            )
            ranking += 1
        else: 
            print(f'Alert! {stats.expansion.code}: No CGV')
    print('Updated CGV Rankings')
    return

def save_gl_rankings():
    today = date.today()
    days_7_ago = today - timedelta(days=7)
    m1_ago = today - relativedelta.relativedelta(months=1)

    stats_today = ExpSimulatedPriceStats.objects.filter(date_simulated=today).order_by('-gainloss')
    stats_7d_ago =  ExpSimulatedPriceStats.objects.filter(date_simulated=days_7_ago).order_by('-gainloss')
    stats_1m_ago =  ExpSimulatedPriceStats.objects.filter(date_simulated=m1_ago).order_by('-gainloss')

    stats_7d_ago_dict = {stat.expansion.code: stat.gainloss for stat in stats_7d_ago}
    stats_1m_ago_dict = {stat.expansion.code: stat.gainloss for stat in stats_1m_ago}
    ranking = 1
    
    for stats in stats_today:
        exp_code = stats.expansion.code
        if stats.gainloss != None:
            today_gainloss = round(stats.gainloss, 2)
            
            # Calculate the 7-day change
            chance_7d_ago = stats_7d_ago_dict.get(exp_code)
            change_7d_percent = calculate_change(today_gainloss, chance_7d_ago)
            
            # Calculate the 1-month change
            chance_1m_ago = stats_1m_ago_dict.get(exp_code)
            change_1m_percent = calculate_change(today_gainloss, chance_1m_ago)
            
            # Calculate the all-time change
            first_gainloss = ExpSimulatedPriceStats.objects.values_list('gainloss', flat=True).filter(expansion__code=exp_code).order_by('date_simulated').first()
            change_all_time_percent = calculate_change(today_gainloss, first_gainloss)

            ExpRankings.objects.update_or_create(
                expansion = stats.expansion,
                ranking_date = today,
                defaults = {
                    'gl_ranking': ranking,
                    'gl_today': today_gainloss,
                    'gl_week': change_7d_percent,
                    'gl_month': change_1m_percent,
                    'gl_all_time': change_all_time_percent,
                }
            )
            ranking += 1
        else: 
            print(f'Alert! {stats.expansion.code}: No gainloss')
    print('Updated GainLoss Rankings')
    return

def update_ranking_change():
    today = date.today()
    last_ranking_date = ExpRankings.objects.values_list('ranking_date', flat=True).filter(ranking_date__lt=today).order_by('-ranking_date').first()        
    todayrankings = ExpRankings.objects.filter(ranking_date=today)
    last_rankings = ExpRankings.objects.filter(ranking_date=last_ranking_date)

    for ranking in todayrankings:
        cgv_rank_today = ranking.cgv_ranking
        cgv_rank_last = last_rankings.filter(expansion=ranking.expansion) 
        if cgv_rank_last.exists():
            cgv_rank_last = cgv_rank_last.first().cgv_ranking
        else: 
            cgv_rank_last = cgv_rank_today
        cgv_ranking_change = cgv_rank_last - cgv_rank_today
        ranking.cgv_ranking_change = cgv_ranking_change

        gl_rank_today = ranking.gl_ranking
        gl_rank_last = last_rankings.filter(expansion=ranking.expansion)
        if gl_rank_last.exists():
            gl_rank_last = gl_rank_last.first().gl_ranking
        else:
            gl_rank_last = gl_rank_today
        gl_ranking_change = gl_rank_last - gl_rank_today
        ranking.gl_ranking_change = gl_ranking_change
        ranking.save()
    print('updated ranking changes')