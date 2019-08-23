from django.shortcuts import render, redirect
from .forms import CustomUserChangeOnlyTwoForm


def profileview(request):
    context = {'user': request.user}
    return render(request, 'profile_view.html', context)


def profileedit(request):
    if request.method == 'POST':
        form = CustomUserChangeOnlyTwoForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile_view')
        else:
            return render(request, 'profile_edit.html', {'form': form})
    else:
        form = CustomUserChangeOnlyTwoForm(instance=request.user)
        context = {'form': form}
        return render(request, 'profile_edit.html', context)
