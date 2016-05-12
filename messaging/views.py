from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings

from base.models import Message, Person, Nurse, Logger
from .forms import ComposeForm
from .utils import format_quote, get_user_model, get_username_field

User = get_user_model()

if "notification" in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
    from notification import models as notification
else:
    notification = None


@login_required
def inbox(request, template_name='messaging/inbox.html'):
    """
    Displays a list of received messages for the current user.
    Optional Arguments:
        ``template_name``: name of the template to use.
    """
    user_model = User.objects.get_by_natural_key(request.user.username)
    sender = Person.objects.get(user=user_model)
    message_list = Message.objects.inbox_for(sender)

    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))


@login_required
def outbox(request, template_name='messaging/outbox.html'):
    """
    Displays a list of sent messages by the current user.
    Optional arguments:
        ``template_name``: name of the template to use.
    """
    user_model = User.objects.get_by_natural_key(request.user.username)
    user = Person.objects.get(user=user_model)
    message_list = Message.objects.outbox_for(user)

    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))


@login_required
def trash(request, template_name='django_messages/trash.html'):
    """
    Displays a list of deleted messages.
    Optional arguments:
        ``template_name``: name of the template to use
    Hint: A Cron-Job could periodical clean up old messages, which are deleted
    by sender and recipient.
    """
    message_list = Message.objects.trash_for(request.user)
    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))


@login_required
def compose(request, recipient=None, form_class=ComposeForm,
            template_name='messaging/compose.html', success_url=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a person, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successful submission
    """
    if request.method == "POST":
        user_model = User.objects.get_by_natural_key(request.user.username)
        sender = Person.objects.get(user=user_model)

        form = form_class(request.POST, recipient_filter=None)
        if form.is_valid():
            form.save(sender=sender)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages:inbox')
            if 'next' in request.GET:
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
            Logger.createLog('Message',sender,form.recipient,None)
    else:
        form = form_class(recipient_filter=setRecipFilter(request))
        if recipient is not None:
            # recipients = [u for u in User.objects.filter(
            #     **{'%s__in' % get_username_field(): [r.strip() for r in recipient.split('+')]})]
            form.fields['recipient'].initial = recipient
    return render_to_response(template_name, {'form': form, }
                              , context_instance=RequestContext(request))


@login_required
def reply(request, message_id, form_class=ComposeForm,
          template_name='messaging/compose.html', success_url=None,
          recipient_filter=None, quote_helper=format_quote,
          subject_template=_(u"Re: %(subject)s"), ):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote. To change the quote format
    assign a different ``quote_helper`` kwarg in your url-conf.

    """
    parent = get_object_or_404(Message, id=message_id)
    user_model = User.objects.get_by_natural_key(request.user.username)
    user = Person.objects.get(user=user_model)

    if parent.sender != user and parent.recipient != user:
        raise Http404

    if request.method == "POST":
        #  The user sent the message
        sender = user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=sender, parent_msg=parent)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages:inbox')
            Logger.createLog('Message',sender,form.recipient,None)    
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(recipient_filter=setRecipFilter(request),
                          initial={
                              'body': '',
                              'subject': subject_template % {'subject': parent.subject},
                              'recipient': parent.sender
                          })
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))


def setRecipFilter(request):
    if request.user.groups.filter(name='Patient').exists():
        return 'Patient'
    elif request.user.groups.filter(name='Root').exists():
        return 'Root'
    elif request.user.groups.filter(name='Doctor').exists():
        return 'Doctor'
    elif request.user.groups.filter(name='Nurse').exists():
        return 'Nurse'
    elif request.user.groups.filter(name='Admin').exists():
        return 'Admin'
    else:
        return None


@login_required
def delete(request, message_id, success_url=None):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete a message
    before it's save to remove it completely.
    A cron-job should prune the database and remove old messages which are
    deleted by both users.
    As a side effect, this makes it easy to implement a trash with undelete.

    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
    page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
    """
    user_model = User.objects.get_by_natural_key(request.user.username)
    user = Person.objects.get(user=user_model)

    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    deleted = False
    if success_url is None:
        success_url = reverse('messages:inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = now
        deleted = True
    if message.recipient == user:
        message.recipient_deleted_at = now
        deleted = True
    if deleted:
        message.save()
        messages.info(request, _(u"Message successfully deleted."))
        if notification:
            notification.send([user], "messages_deleted", {'message': message, })
        return HttpResponseRedirect(success_url)
    raise Http404


@login_required
def undelete(request, message_id, success_url=None):
    """
    Recovers a message from trash. This is achieved by removing the
    ``(sender|recipient)_deleted_at`` from the model.
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    undeleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = None
        undeleted = True
    if message.recipient == user:
        message.recipient_deleted_at = None
        undeleted = True
    if undeleted:
        message.save()
        messages.info(request, _(u"Message successfully recovered."))
        if notification:
            notification.send([user], "messages_recovered", {'message': message, })
        return HttpResponseRedirect(success_url)
    raise Http404


@login_required
def view(request, message_id, form_class=ComposeForm, quote_helper=format_quote,
         subject_template=_(u"Re: %(subject)s"),
         template_name='messaging/view.html'):
    """
    Shows a single message.``message_id`` argument is required.
    The user is only allowed to see the message, if he is either
    the sender or the recipient. If the user is not allowed a 404
    is raised.
    If the user is the recipient and the message is unread
    ``read_at`` is set to the current datetime.
    If the user is the recipient a reply form will be added to the
    template context, otherwise 'reply_form' will be None.
    """
    user_model = User.objects.get_by_natural_key(request.user.username)
    user = Person.objects.get(user=user_model)

    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.recipient != user):
        raise Http404
    if message.read_at is None and message.recipient == user:
        message.read_at = now
        message.save()

        # Grab the first and last initials
    personUser = message.sender.user

    fullName = personUser.get_full_name()
    nameArray = fullName.split()
    firstName = nameArray[0]
    lastName = nameArray[1]
    print(lastName)
    initials = firstName[0] + lastName[0]

    received = False
    context = {'message': message, 'reply_form': None, 'initials': initials, 'received': received}
    if message.recipient == user:
        form = form_class(initial={
            'body': ' ',
            'subject': subject_template % {'subject': message.subject},
            'recipient': message.sender,
        },
        )
        context['reply_form'] = form
        context['received'] = True
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))
