from django.contrib import admin
from django.contrib import messages
from flight.models import *
from django import forms
from gfsa.settings import *
import datetime
from xero.views import *
from xero.email import *
from ajax_select import make_ajax_field
from ajax_select.admin import AjaxSelectAdmin

class GliderFlarmTimeAdmin(admin.ModelAdmin):
    list_display = ['flarm_id', 'flight_record_id', 'take_off', 'landing']


class TugFlarmTimeAdmin(admin.ModelAdmin):
    list_display = ['flarm_id', 'flight_record_id', 'take_off', 'landing']



class GliderFlarmTimeInline(admin.TabularInline):
    model = GfsaGliderFlarmFlightRecords
    can_delete = False
    exclude = ('flarm_id',)
    readonly_fields = ('take_off', 'landing',)
    extra = 0
    class Meta:
        #css = {'all': ('css/no-addanother-button.css',)}
        verbose_name_plural = 'Glider Times from Flarm'


class TugFlarmTimeInline(admin.TabularInline):
    model = GfsaTugFlarmFlightRecords
    can_delete = False
    exclude = ('flarm_id',)
    readonly_fields = ('take_off', 'landing',)
    extra = 0
    class Meta:
        #css = {'all': ('css/no-addanother-button.css',)}
        verbose_name_plural = 'Tug Times from Flarm'


# Create the form class.
class AddFlightRecordForm(forms.ModelForm):
    fr_p1_id = make_ajax_field(GfsaFlightRecords,'fr_p1_id','person')
    fr_p2_id = make_ajax_field(GfsaFlightRecords,'fr_p2_id','person')
    fr_p1_pay_percent = forms.ChoiceField(choices=PAY_PERCENT, required=False, initial='100')
    fr_p2_pay_percent = forms.ChoiceField(choices=PAY_PERCENT, required=False, initial='0')

    def clean(self):
        cleaned_data = super(AddFlightRecordForm, self).clean()
        try:
            glider = GfsaGliders.objects.get(pk=cleaned_data.get('glider_glider').pk)
        except:
            msg = u'Glider already flew off'
            raise forms.ValidationError(msg, cleaned_data)
        if str(glider.glider_seat_type) == str(1):
            if cleaned_data.get('fr_p1_id') != '':

                if cleaned_data.get('fr_p2_id') != None:
                    if cleaned_data.get('fr_p2_pay_percent') != 0:
                        msg = u'Gilder 1 Seat Only. Select one pilot and one payment'
                    del cleaned_data['fr_p2_id']
                    raise forms.ValidationError(msg, cleaned_data)
        if cleaned_data.get('fr_p2_id') == None and int(cleaned_data.get('fr_p2_pay_percent')) != 0:
            msg = u'Please select appropriate pay percentages'
            raise forms.ValidationError(msg, cleaned_data)
        if int(cleaned_data.get('fr_p1_pay_percent')) + int(cleaned_data.get('fr_p2_pay_percent')) != 100:
            msg = u'Please select appropriate pay percentages'
            raise forms.ValidationError(msg, cleaned_data)
        print cleaned_data.get('fr_p1_id')
        print cleaned_data.get('fr_p2_id')
        if cleaned_data.get('fr_p1_id') == cleaned_data.get('fr_p2_id'):
            msg = u'Please select different pilots'
            raise forms.ValidationError(msg, cleaned_data)
        
        return cleaned_data

    class Meta:
        model = GfsaFlightRecords
        fields = ['glider_glider', 'fr_p1_id', 'fr_p2_id', 'fr_p1_pay_percent', 'fr_p2_pay_percent', 'fr_comment']


class GfsaFlightRecordsAdmin(admin.ModelAdmin):
    form = AddFlightRecordForm
    search_fields = ['glider_glider__glider_identifier']
    list_display = ['fr_id', 'glider', 'fr_p1_id', 'fr_p2_id']
    date_hierarchy = 'fr_created'
    list_per_page = 20


    def glider(self, obj):
        glider = GfsaGliders.objects.get(glider_id=obj.glider_glider.glider_id)
        return u'%s' % glider.glider_identifier

    def queryset(self, request):
        qs = super(admin.ModelAdmin, self).queryset(request)
        return qs.filter(fr_take_off__isnull=True)

    def save_model(self, request, obj, form, change):

        msg = u'Gilder %s Ready for take off' % (obj.glider_glider)
        messages.info(request, msg)
        super(GfsaFlightRecordsAdmin, self).save_model(request, obj, form, change)

class TakeOffForm(forms.ModelForm):
    pass

    def clean(self):
        cleaned_data = super(TakeOffForm, self).clean()
        # here is an error
        try:
            tug = GfsaTugs.objects.get(pk=cleaned_data.get('tug_tug').pk)
        except:
            msg = u'Tug already flew off'
            raise forms.ValidationError(msg, cleaned_data)
        if str(tug.tug_status) == 'In Flight':
            msg = u'Tug already flew off'
            del cleaned_data['tug_tug']
            raise forms.ValidationError(msg, cleaned_data)
        return cleaned_data

    class Meta:
        model = GfsaTakeOff
        fields = ['tug_tug', 'fr_id']


class GfsaFlightRecordsTakeOffAdmin(admin.ModelAdmin):
    form = TakeOffForm
    fields = ('tug_tug',)
    search_fields = ['fr_p1_id__last_name','fr_p1_id__first_name','fr_p2_id__last_name','fr_p2_id__first_name','glider_glider__glider_identifier']
    list_filter = []
    list_display = ['glider', 'fr_p1_id', 'fr_p2_id', 'fr_created']
    date_hierarchy = 'fr_created'
    change_form_template = 'admin/flight/change_form_take_off.html'
    can_delete = False

    def glider(self, obj):
        glider = GfsaGliders.objects.get(glider_id=obj.glider_glider.glider_id)
        return u'%s' % glider.glider_identifier

    def queryset(self, request):
        qs = super(admin.ModelAdmin, self).queryset(request)
        return qfr_tug_durations.filter(fr_take_off__isnull=True).order_by("fr_created")

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):

        flight_record = GfsaFlightRecords.objects.get(pk=obj.pk)
        p1_flying = GfsaFlightRecords.objects.filter(fr_glider_land__isnull = True,fr_take_off__isnull= False,fr_p1_id = flight_record.fr_p1_id).exclude(pk=obj.pk)
        if flight_record.glider_glider.glider_status == 'In Flight':
            msg = u'Glider %s is flying' % (flight_record.glider_glider.glider_identifier)
            messages.add_message(request, messages.ERROR, msg)  
        
        elif len(p1_flying) !=  0:
            msg = u'Member(P1) %s is still flying' % (flight_record.fr_p1_id)
            messages.add_message(request, messages.ERROR, msg) 
            if flight_record.fr_p2_id is not None:
                p2_flying = GfsaFlightRecords.objects.filter(fr_glider_land__isnull = True,fr_take_off__isnull= False,fr_p2_id = flight_record.fr_p2_id).exclude(pk=obj.pk)
                if len(p2_flying) is not 0: 
                    msg = u'Member(P2) %s is still flying' % (flight_record.fr_p2_id)
                    messages.add_message(request, messages.ERROR, msg) 
        else:
            flight_record.tug_tug = obj.tug_tug
            flight_record.fr_take_off = datetime.datetime.now()
            flight_record.save()
            glider_flarm = GfsaGliderFlarmFlightRecords()
            glider_flarm.flight_record_id = obj
            glider_flarm.flarm_id = obj.glider_glider.glider_flarm_id
            glider_flarm.save()
            glider = GfsaGliders.objects.get(glider_id=obj.glider_glider.glider_id)
            glider.glider_status = 'In Flight'
            glider.save()
            tug = GfsaTugs.objects.get(tug_id=obj.tug_tug.tug_id)
            tug.tug_status = 'In Flight'
            tug.save()
            tug_flarm = GfsaTugFlarmFlightRecords()
            tug_flarm.flight_record_id = obj
            tug_flarm.flarm_id = obj.tug_tug.tug_flarm_id
            tug_flarm.save()
            msg = u'Gilder %s took off with Tug %s' % (obj.glider_glider, obj.tug_tug)
            messages.add_message(request, messages.INFO, msg)  



class GfsaFlightRecordsTugLandingAdmin(admin.ModelAdmin):
    fields = ('tug_tug', 'fr_take_off',)
    search_fields = ['tug_tug__tug_identifier']
    list_filter = []
    readonly_fields = ['tug_tug', 'fr_take_off', ]
    list_display = ['tug', 'fr_take_off']
    date_hierarchy = 'fr_created'
    change_form_template = 'admin/flight/change_form_landing.html'
    can_delete = False

    def tug(self, obj):
        tug = GfsaTugs.objects.get(tug_id=obj.tug_tug.tug_id)
        return u'%s' % tug.tug_identifier

    def queryset(self, request):
        qs = super(admin.ModelAdmin, self).queryset(request)
        return qs.filter(fr_take_off__isnull=False).exclude(fr_tug_land__isnull=False)

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        flight_record = GfsaFlightRecords.objects.get(pk=obj.pk)
        flight_record.fr_tug_land = datetime.datetime.now()
        now = datetime.datetime.now()
        take_off = flight_record.fr_take_off
        duration = str((now - take_off).seconds)
        flight_record.fr_tug_duration = duration
        flight_record.save()

        tug = GfsaTugs.objects.get(tug_id=obj.tug_tug.tug_id)
        tug.tug_status = 'Ready'
        tug.save()
        msg = u'Tug %s has landed' % (obj.tug_tug)
        messages.info(request, msg)




class GfsaFlightRecordsGliderLandingAdmin(admin.ModelAdmin):
    fields = ('glider_glider', 'fr_p1_id', 'fr_p2_id', 'fr_take_off',)
    search_fields = ['fr_p1_id__last_name','fr_p1_id__first_name','fr_p2_id__last_name','fr_p2_id__first_name','glider_glider__glider_identifier']
    list_filter = []
    readonly_fields = ['glider_glider', 'fr_p1_id', 'fr_p2_id', 'fr_take_off', ]
    list_display = ['glider', 'fr_p1_id', 'fr_p2_id', 'fr_take_off']
    date_hierarchy = 'fr_created'
    change_form_template = 'admin/flight/change_form_landing.html'
    can_delete = False


    def glider(self, obj):
        glider = GfsaGliders.objects.get(glider_id=obj.glider_glider.glider_id)
        return u'%s' % glider.glider_identifier

    def queryset(self, request):
        qs = super(admin.ModelAdmin, self).queryset(request)
        return qs.filter(fr_take_off__isnull=False).exclude(fr_glider_land__isnull=False)

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        flight_record = GfsaFlightRecords.objects.get(pk=obj.pk)

        flight_record.fr_glider_land = datetime.datetime.now()
        now = datetime.datetime.now()
        take_off = flight_record.fr_take_off
        duration = str((now - take_off).seconds)
        flight_record.fr_glider_duration = duration
        flight_record.save()
        glider = GfsaGliders.objects.get(glider_id=obj.glider_glider.glider_id)
        glider.glider_status = 'Ready'
        glider.save()
        msg = u'Glider %s has landed' % (obj.glider_glider)
        messages.info(request, msg)



class GfsaFlightRecordSheetAdmin(admin.ModelAdmin):
    change_list_template = 'admin/flight/change_list_flightsheet.html'
    search_fields = ['fr_p1_id__last_name','fr_p1_id__first_name','fr_p2_id__last_name','fr_p2_id__first_name','glider_glider__glider_identifier','tug_tug__tug_identifier','fr_comment']
    list_display = ['fr_id', 'created',  'fr_p1_id', 'fr_p2_id', 'fr_p1_pay_percent',
                    'fr_p2_pay_percent', 'tug_tug', 'glider_glider','take_off', 'tug_land', 'tug_duration', 'glider_land',
                    'glider_duration', 'fr_comment']
    date_hierarchy = 'fr_created'
    list_filter = ['fr_created', 'tug_tug', 'glider_glider', 'fr_in_xero']
    exclude = ['fr_tug_duration', 'fr_glider_duration']
    inlines = [GliderFlarmTimeInline, TugFlarmTimeInline]
    can_delete = False
    def take_off(self,obj):
        try:
            return obj.fr_take_off.strftime('%d.%m.%y %H:%M')
        except:
            return '(None)'
    take_off.short_description = 'Take Off'
    take_off.admin_order_field = 'fr_take_off'
    def created(self,obj):
        try:
            return obj.fr_created.strftime('%d.%m.%y %H:%M')
        except:
            return '(None)'
    created.short_description = 'Created'
    created.admin_order_field = 'fr_created'
    def tug_land(self,obj):
        try:
            return obj.fr_tug_land.strftime('%d.%m.%y %H:%M')
        except:
            return '(None)'
    tug_land.short_description = 'Tug Landing Time'
    tug_land.admin_order_field = 'fr_tug_land'

    def glider_land(self,obj):
        try:
            return obj.fr_glider_land.strftime('%d.%m.%y %H:%M')
        except:
            return '(None)'
    glider_land.short_description = 'Glider Landing Time'
    glider_land.admin_order_field = 'fr_glider_land'

    def save_model(self, request, obj, form, change):
        try:
            glider_flarm = GfsaGliderFlarmFlightRecords.objects.get(flight_record_id=obj)
        except:
            glider_flarm = GfsaGliderFlarmFlightRecords()
            glider_flarm.flight_record_id = obj
            glider_flarm.flarm_id = obj.glider_glider.glider_flarm_id
            glider_flarm.save()
        try:
            tug_flarm = GfsaTugFlarmFlightRecords.objects.get(flight_record_id=obj)
        except:
            tug_flarm = GfsaTugFlarmFlightRecords()
            tug_flarm.flight_record_id = obj
            tug_flarm.flarm_id = obj.tug_tug.tug_flarm_id
            tug_flarm.save()

        if obj.fr_glider_land == None or obj.fr_take_off == None or obj.fr_tug_land == None:
            obj.fr_glider_duration = None  
            obj.fr_tug_duration = None
        
        else:
            total_glider_duration = (obj.fr_glider_land - obj.fr_take_off).seconds 
            obj.fr_glider_duration = total_glider_duration if total_glider_duration > 0 else None

            total_tug_duration = (obj.fr_tug_land - obj.fr_take_off).seconds
            obj.fr_tug_duration = total_tug_duration if total_tug_duration > 0 else None

        obj.save()

    def tug_duration(self, obj):
        try:
            total =(obj.fr_tug_land-obj.fr_take_off).seconds
            duration =  u'%s'  %  str(datetime.timedelta(seconds=total))
        except:
            duration = 'N/A'
        return duration

    tug_duration.short_description = 'Tug duration'

    def glider_duration(self, obj):
        try:
            total =(obj.fr_glider_land-obj.fr_take_off).seconds
            duration =  u'%s'  %  str(datetime.timedelta(seconds=total))
        except:
            duration = 'N/A'
        return duration

    glider_duration.short_description = 'Gilder duration'

    def glider(self, obj):
        glider = GfsaGliders.objects.get(glider_id=obj.glider_glider.glider_id)
        return u'%s' % glider.glider_identifier

    def tug(self, obj):
        tug = GfsaTugs.objects.get(tug_id=obj.tug_tug.tug_id)
        return u'%s' % tug.tug_identifier

    actions = ['send_flight_notification', 'upload_to_xero']

    def send_flight_notification(self, request, queryset):
        for flight_record in queryset:
            tug_duration = flight_record.fr_tug_duration
            glider_duration = flight_record.fr_glider_duration
            p1 = str(flight_record.fr_p1_id)
            p2 = str(flight_record.fr_p2_id)
            p1_pay_percent = int(flight_record.fr_p1_pay_percent)
            p2_pay_percent = int(flight_record.fr_p2_pay_percent)

            send_sms_p1 = False
            send_sms_p2 = False
            p1_mobile = ''
            p2_mobile = ''

            if tug_duration is None or glider_duration is None:
                msg = u'Cannot send! Flight Record %s is not completed.' % (flight_record.fr_id)
                messages.info(request, msg)

            elif flight_record.fr_sent == True:
                msg = u'Send failed! Flight Record %s is already sent.' % (flight_record.fr_id)
                messages.info(request, msg)

            elif flight_record.fr_sent == False:
                send_p1 = True
                send_p2 = True
                tug_duration = int(flight_record.fr_tug_duration)/60.0
                glider_duration = int(flight_record.fr_glider_duration)/60
                notification = p1 + ' pays ' + str(p1_pay_percent) + '% ' + p2 + ' pays ' + str(p2_pay_percent) + '% ' + \
                ' Tug Duration: ' + str(tug_duration) + ' Glider Duration: ' +\
                str(glider_duration) + ' Comment: ' + str(flight_record.fr_comment)
                try:
                    member_p1 = GFSAXeroContactPerson.objects.get(contact_name=p1)
                    p1_mobile = member_p1.phone
                    if p1_mobile is not None:
                        send_sms_p1 = True
                    if not member_p1.in_xero:
                        send_p1 = False
                except:
                    send_p1 = False
                try:
                    member_p2 = GFSAXeroContactPerson.objects.get(contact_name=p2)
                    p2_mobile = member_p2.phone
                    if p2_mobile is not None:
                        send_sms_p2 = True
                    if not member_p2.in_xero:
                        send_p2 = False
                except:
                    send_p2 = False
                if send_p1 == True:
                    if email_anyone(member_p1.email_address, notification):
                        queryset.update(fr_sent=True)

                if send_p2 == True:
                    if email_anyone(member_p2.email_address, notification):
                        queryset.update(fr_sent=True)

                if send_sms_p1:

                    if send_SMS(p1_mobile, notification):
                        queryset.update(fr_sent=True)

                if send_sms_p2:
                    if send_SMS(p2_mobile, notification):
                        queryset.update(fr_sent=True)

    send_flight_notification.short_description = "Notify Members"


    def upload_to_xero(self, request, queryset):

        tug_flag_solo_prefix = "FTSV"
        tug_flag_mutual_prefix = "FTMV"
        tug_solo_prefix = "TSV"
        tug_mutual_prefix = "TMV"
        glider_flag_solo_prefix = "FGSV"
        glider_flag_mutual_prefix = "FGMV"
        glider_solo_prefix = "GSV"
        glider_mutual_prefix = "GMV"

        discountRate = 0

        inv_type = 'ACCREC'

        description = ''

        for flight_record in queryset:

            tug_duration = flight_record.fr_tug_duration
            glider_duration = flight_record.fr_glider_duration

            p1 = str(flight_record.fr_p1_id)
            p2 = str(flight_record.fr_p2_id)
            p1_pay_percent = int(flight_record.fr_p1_pay_percent)
            p2_pay_percent = int(flight_record.fr_p2_pay_percent)
            

            if tug_duration is None or glider_duration is None:
                msg = u'Cannot Upload! Flight Record %s is not completed.' % (flight_record.fr_id)
                messages.info(request, msg)

            elif flight_record.fr_in_xero == True:
                msg = u'Cannot Upload! Flight Record %s is already in xero.' % (flight_record.fr_id)
                messages.info(request, msg)

            elif flight_record.fr_in_xero == False:

                tug_duration = int(tug_duration)/60.0
                glider_duration = int(glider_duration)/60.0

                if tug_duration > MAX_DURATION:
                    tug_duration = MAX_DURATION
                if glider_duration > MAX_DURATION:
                    glider_duration = MAX_DURATION

                if p1_pay_percent == 50 and p2_pay_percent == 50:

                    description += p1 + ' ' + str(p1_pay_percent) + ' ' + p2 + ' ' + str(p2_pay_percent) + ' ' + \
                                   str(flight_record.glider_glider) + ' ' + str(flight_record.tug_tug) + ' ' + \
                                   str(flight_record.fr_take_off) + ' ' + str(flight_record.fr_tug_land) + ' ' + \
                                   str(tug_duration) + ' ' + str(flight_record.fr_glider_land) + ' ' + \
                                   str(glider_duration) + ' ' + str(flight_record.fr_comment) + '\n'

                    tug_flag_mutual = tug_flag_mutual_prefix + str(flight_record.tug_tug)
                    tug_mutual = tug_mutual_prefix + str(flight_record.tug_tug)
                    glider_flag_mutual = glider_flag_mutual_prefix + str(flight_record.glider_glider)
                    glider_mutual = glider_mutual_prefix + str(flight_record.glider_glider)

                    flag = False
                    send_p1 = True
                    send_p2 = True

                    try:
                        member_p1 = GFSAXeroContactPerson.objects.get(contact_name=p1)
                        if not member_p1.in_xero:
                            msg = u'Invoice of %s Cannot Be Uploaded because %s is not in xero.' % (
                                flight_record.fr_p1_id, flight_record.fr_p1_id)
                            messages.info(request, msg)
                            send_p1 = False

                    except:
                        msg = "%s is not in database!" % (p1)
                        messages.info(request, msg)
                        print msg
                        send_p1 = False

                    try:
                        member_p2 = GFSAXeroContactPerson.objects.get(contact_name=p2)
                        if not member_p2.in_xero:
                            msg = u'Invoice of %s Cannot Be Uploaded because %s is not in xero.' % (
                                flight_record.fr_p2_id, flight_record.fr_p2_id)
                            messages.info(request, msg)
                            send_p2 = False

                    except:
                        msg = "%s is not in database!" % (p2)
                        messages.info(request, msg)
                        print msg
                        send_p2 = False

                    try:
                        GFSAXeroItemCode.objects.get(item_code=tug_flag_mutual)
                    except:
                        msg = u'Flight record %s Cannot Be Uploaded! Itemcode %s is not in xero.' % (
                            flight_record.fr_id, tug_flag_mutual)
                        messages.info(request, msg)
                        flag = True

                    try:
                        GFSAXeroItemCode.objects.get(item_code=tug_mutual)
                    except:
                        msg = u'Flight record %s Cannot Be Uploaded! Itemcode %s is not in xero.' % (
                            flight_record.fr_id, tug_mutual)
                        messages.info(request, msg)
                        flag = True

                    try:
                        GFSAXeroItemCode.objects.get(item_code=glider_flag_mutual)
                    except:
                        msg = u'Flight record %s Cannot Be Uploaded! Itemcode %s is not in xero.' % (
                            flight_record.fr_id, glider_flag_mutual)
                        messages.info(request, msg)
                        flag = True

                    try:
                        GFSAXeroItemCode.objects.get(item_code=glider_mutual)
                    except:
                        msg = u'Flight record %s Cannot Be Uploaded! Itemcode %s is not in xero.' % (
                            flight_record.fr_id, glider_mutual)
                        messages.info(request, msg)
                        flag = True 

                    if not flag:

                        tug_flag_mutual_item = get_item_line(tug_flag_mutual, 1, discountRate, description)
                        tug_mutual_item = get_item_line(tug_mutual, tug_duration, discountRate, description)
                        glider_flag_mutual_item = get_item_line(glider_flag_mutual, 1, discountRate,
                                                                description)
                        glider_mutual_item = get_item_line(glider_mutual, glider_duration, discountRate, description)
                        line_items = [tug_flag_mutual_item, tug_mutual_item, glider_flag_mutual_item,
                                      glider_mutual_item]
                        contact_p1 = get_contact_name(p1)
                        contact_p2 = get_contact_name(p2)
                        p1_inv = get_invoice(inv_type, contact_p1, line_items)
                        p2_inv = get_invoice(inv_type, contact_p2, line_items)
                        if send_p1:
                            if upload(request, p1_inv):
                                msg = u'Invoice of %s has been uploaded to xero successfully.' % (p1)
                                messages.info(request, msg)
                                queryset.update(fr_in_xero=True)
                            else:
                                msg = u'Invoice of %s failed to upload to xero.' % (p1)
                                messages.info(request, msg)
                        if send_p2:
                            if upload(request, p2_inv):
                                msg = u'Invoice of %s has been uploaded to xero successfully.' % (p2)
                                messages.info(request, msg)
                                queryset.update(fr_in_xero=True)
                            else:
                                msg = u'Invoice of %s failed to upload to xero.' % (p2)
                                messages.info(request, msg)


                elif p1_pay_percent == 100 or p2_pay_percent == 100:

                    description += p1 + ' ' + str(p1_pay_percent) + ' ' + p2 + ' ' + str(p2_pay_percent) + ' ' + \
                                   str(flight_record.glider_glider) + ' ' + str(flight_record.tug_tug) + ' ' + \
                                   str(flight_record.fr_take_off) + ' ' + str(flight_record.fr_tug_land) + ' ' + \
                                   str(tug_duration) + ' ' + str(flight_record.fr_glider_land) + ' ' + \
                                   str(glider_duration) + ' ' + str(flight_record.fr_comment) + '\n'

                    tug_flag_solo = tug_flag_solo_prefix + str(flight_record.tug_tug)
                    tug_solo = tug_solo_prefix + str(flight_record.tug_tug)
                    glider_flag_solo = glider_flag_solo_prefix + str(flight_record.glider_glider)
                    glider_solo = glider_solo_prefix + str(flight_record.glider_glider)

                    flag = False

                    try:
                        GFSAXeroItemCode.objects.get(item_code=tug_flag_solo)
                    except:
                        msg = u'Flight record %s Cannot Be Uploaded! Itemcode %s is not in xero.' % (
                            flight_record.fr_id, tug_flag_solo)
                        messages.info(request, msg)
                        flag = True

                    try:
                        GFSAXeroItemCode.objects.get(item_code=tug_solo)
                    except:
                        msg = u'Flight record %s Cannot Be Uploaded! Itemcode %s is not in xero.' % (
                            flight_record.fr_id, tug_solo)
                        messages.info(request, msg)
                        flag = True

                    try:
                        GFSAXeroItemCode.objects.get(item_code=glider_flag_solo)
                    except:
                        msg = u'Flight record %s Cannot Be Uploaded! Itemcode %s is not in xero.' % (
                            flight_record.fr_id, glider_flag_solo)
                        messages.info(request, msg)
                        flag = True

                    try:
                        GFSAXeroItemCode.objects.get(item_code=glider_solo)
                    except:
                        msg = u'Flight record %s Cannot Be Uploaded! Itemcode %s is not in xero.' % (
                            flight_record.fr_id, glider_solo)
                        messages.info(request, msg)
                        flag = True

                    if not flag:
                        if p1_pay_percent == 100:

                            try:
                                member_p1 = GFSAXeroContactPerson.objects.get(contact_name=p1)
                                tug_flag_solo_item = get_item_line(tug_flag_solo, 1, discountRate,
                                                                   description)
                                tug_solo_item = get_item_line(tug_solo, tug_duration, discountRate, description)
                                glider_flag_solo_item = get_item_line(glider_flag_solo, 1, discountRate,
                                                                      description)
                                glider_solo_item = get_item_line(glider_solo, glider_duration, discountRate,
                                                                 description)
                                line_items = [tug_flag_solo_item, tug_solo_item, glider_flag_solo_item,
                                              glider_solo_item]
                                contact_p1 = get_contact_name(p1)
                                p1_inv = get_invoice(inv_type, contact_p1, line_items)
                                if not member_p1.in_xero:
                                    msg = u'Invoice of %s Cannot Be Uploaded because %s is not in xero.' % (
                                        flight_record.fr_p1_id, flight_record.fr_p1_id)
                                    messages.info(request, msg)
                                else:
                                    if upload(request, p1_inv):
                                        msg = u'Invoice of %s has been uploaded to xero successfully.' % (p1)
                                        messages.info(request, msg)
                                        queryset.update(fr_in_xero=True)
                                    else:
                                        msg = u'Invoice of %s failed to upload to xero.' % (p1)
                                        messages.info(request, msg)
                            except:
                                print "No this member in database!"

                        else:

                            try:
                                member_p2 = GFSAXeroContactPerson.objects.get(contact_name=p2)
                                tug_flag_solo_item = get_item_line(tug_flag_solo, 1, discountRate,
                                                                   description)
                                tug_solo_item = get_item_line(tug_solo, tug_duration, discountRate, description)
                                glider_flag_solo_item = get_item_line(glider_flag_solo, 1, discountRate,
                                                                      description)
                                glider_solo_item = get_item_line(glider_solo, glider_duration, discountRate,
                                                                 description)
                                line_items = [tug_flag_solo_item, tug_solo_item, glider_flag_solo_item,
                                              glider_solo_item]
                                contact_p2 = get_contact_name(p2)
                                p2_inv = get_invoice(inv_type, contact_p2, line_items)

                                if not member_p2:
                                    msg = u'Invoice of %s Cannot Be Uploaded because %s is not in xero.' % (
                                        flight_record.fr_p2_id, flight_record.fr_p2_id)
                                    messages.info(request, msg)
                                else:
                                    if upload(request, p2_inv):
                                        msg = u'Invoice of %s has been uploaded to xero successfully.' % (p2)
                                        messages.info(request, msg)
                                        queryset.update(fr_in_xero=True)
                                    else:
                                        msg = u'Invoice of %s failed to upload to xero.' % (p2)
                                        messages.info(request, msg)
                            except:
                                print "No this member in database!"

        if len(description) > 0:
            email_admin(description)                


    upload_to_xero.short_description = "Upload_to_Xero"


admin.site.register(GfsaFlightRecords, GfsaFlightRecordsAdmin)
admin.site.register(GfsaTakeOff, GfsaFlightRecordsTakeOffAdmin)
admin.site.register(GfsaTugLanding, GfsaFlightRecordsTugLandingAdmin)
admin.site.register(GfsaGliderLanding, GfsaFlightRecordsGliderLandingAdmin)
admin.site.register(GfsaFlightRecordSheet, GfsaFlightRecordSheetAdmin)
admin.site.register(GfsaGliderFlarmFlightRecords, GliderFlarmTimeAdmin)
admin.site.register(GfsaTugFlarmFlightRecords, TugFlarmTimeAdmin)

