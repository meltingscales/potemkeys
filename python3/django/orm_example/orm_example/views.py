from django.shortcuts import render

from orm_example.models import PersonForm, Person


def index(request):
    return render(request, "index.html")


def people(request):
    """
    Shows the user a list of all people, and lets them add new ones.

    Also handles HTTP POST from forms.
    """

    # Context to render the Jinja template with.
    context = {}

    # Add all people in DB to context.
    context["people"] = Person.objects.all()

    print(Person.objects.get(pk=2))

    # If they want to make a new person,
    if request.method == "POST":

        # Create a form from the HTTP Request.
        form = PersonForm(request.POST)

        # Check if the form satisfies all the constraints put forth by Person object.
        if form.is_valid():
            form.save()
        else:
            print("Error saving Person.")
            print(form.errors)

            # Give them back their erroneous form.
            context['form'] = form

    # Add form in DB to context if it doesn't exist.
    if 'form' not in context:
        context["form"] = PersonForm()

    # Return `person.html` with a list of all people and a form to add a new person
    return render(request, "person.html", context)
