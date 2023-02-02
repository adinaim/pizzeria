from apps.account.models import UserProfile


def cashback(context, order, total_sum, company):
    user = context['request'].user
    email = user.email
    profile = UserProfile.objects.get(email=email)
    # company = str(company)

    if profile:
        p_cashback = profile.cashback
        if not cashback:
            cashback = 0
            order.total_sum = total_sum
            cashback = total_sum * 0.05
            p_cashback.update(cashback=cashback)
            profile.save()
        else:
            if total_sum >= p_cashback:
                total_sum -= p_cashback
                p_cashback = 0
            else:
                total_sum = 0
                p_cashback -= total_sum
            p_cashback.update(cashback=cashback)
            profile.save()

        order.save()
    
    elif not profile:
        return 'Чтобы накопить баллы, зарегистрируйтесь.'