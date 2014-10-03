from django.shortcuts import render
from xeroapi.api import Xero
from xeroapi.auth import PrivateCredentials
from django.http import HttpResponse
from xero.models import *
from xero.email import *
from flight.models import GfsaFlightRecords
import smtplib
import os
import traceback
from django.shortcuts import redirect
from django.contrib import messages
from clubs.models import *
from xero_config import *


def access_to_xero(request):
    try:
        consumer_key = CONSUMER_KEY
        dir = os.getcwd()
        with open(dir + '/xero/xeroapi/privatekey.pem') as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(consumer_key, rsa_key)
        xero = Xero(credentials)
    except:
        #traceback.print_exc()
        return HttpResponse('<h1>Failed to access to xero</h1>')
    return xero


def get_contacts(request):
    xero = access_to_xero(request)
    try:
        contacts = xero.contacts.all()
    except:
        #traceback.print_exc()
        return HttpResponse('<h1>Failed to update contact list</h1>')

    if type(contacts) == list:
        for contact in contacts:
            xero_contact_person = GFSAXeroContactPerson()
            for (key, value) in contact.iteritems():
                if key == 'ContactID':
                    xero_contact_person.contact_id = value
                elif key == 'Name':
                    xero_contact_person.contact_name = value
                elif key == 'FirstName':
                    xero_contact_person.first_name = value
                elif key == 'LastName':
                    xero_contact_person.last_name = value
                elif key == 'EmailAddress':
                    xero_contact_person.email_address = value
                elif key == 'Phones':
                    xero_contact_person.phone = get_mobile_no(value)

            try:
                local_contact_person = GFSAXeroContactPerson.objects.get(contact_id=xero_contact_person.contact_id)
                # local_contact_person.contact_name = xero_contact_person.contact_name 
                # local_contact_person.first_name = xero_contact_person.first_name
                # local_contact_person.last_name = xero_contact_person.last_name
                # local_contact_person.email_address = xero_contact_person.email_address
                # local_contact_person.phone = xero_contact_person.phone
                # local_contact_person.save()
            except:
                #traceback.print_exc()
                xero_contact_person.in_xero = True
                try:
                    club = GfsaClubs.objects.get(club_name='Melbourne Gliding Club')
                    xero_contact_person.club = club
                except:
                    pass
                xero_contact_person.save()

    elif type(contacts) == dict:
        xero_contact_person = GFSAXeroContactPerson()
        for (key, value) in contacts.iteritems():
            if key == 'ContactID':
                xero_contact_person.contact_id = value
            elif key == 'Name':
                xero_contact_person.contact_name = value
            elif key == 'FirstName':
                xero_contact_person.first_name = value
            elif key == 'LastName':
                xero_contact_person.last_name = value
            elif key == 'EmailAddress':
                xero_contact_person.email_address = value
            elif key == 'Phones':
                xero_contact_person.phone = get_mobile_no(value)
        try:
            local_contact_person = GFSAXeroContactPerson.objects.get(contact_id=xero_contact_person.contact_id)
            # local_contact_person.contact_name = xero_contact_person.contact_name 
            # local_contact_person.first_name = xero_contact_person.first_name
            # local_contact_person.last_name = xero_contact_person.last_name
            # local_contact_person.email_address = xero_contact_person.email_address
            # local_contact_person.phone = xero_contact_person.phone
            # local_contact_person.save()

        except:
            #traceback.print_exc()
            xero_contact_person.in_xero = True
            try:
                club = GfsaClubs.objects.get(club_name='Melbourne Gliding Club')
                xero_contact_person.club = club
            except:
                pass
            xero_contact_person.save()

    if not contacts:
        return HttpResponse('<h1>Empty contact list</h1>')
    return redirect('/admin/xero/gfsaxerocontactperson')


def get_item_code(request):
    xero = access_to_xero(request)
    try:
        item_codes = xero.items.all()
    except:
        #traceback.print_exc()
        return HttpResponse('<h1>Failed to update item code list</h1>')

    if type(item_codes) == list:
        for item_code in item_codes:
            xero_item_code = GFSAXeroItemCode()
            for (key, value) in item_code.iteritems():
                if key == 'ItemID':
                    xero_item_code.item_code_id = value
                if key == 'Code':
                    xero_item_code.item_code = value
            try:
                local_item_code = GFSAXeroItemCode.objects.get(item_code_id=xero_item_code.item_code_id)
                local_item_code.item_code = xero_item_code.item_code
                local_item_code.save()
            except:
                #traceback.print_exc()
                xero_item_code.save()

    elif type(item_codes) == dict:
        xero_item_code = GFSAXeroItemCode()
        for (key, value) in item_codes.iteritems():
            if key == 'ItemID':
                xero_item_code.item_code_id = value
            if key == 'Code':
                xero_item_code.item_code = value
        try:
            local_item_code = GFSAXeroItemCode.objects.get(item_code_id=xero_item_code.item_code_id)
            local_item_code.item_code = xero_item_code.item_code
            local_item_code.save()
        except:
            #traceback.print_exc()
            xero_item_code.save()

    if not item_codes:
        return HttpResponse('<h1>Empty item code list</h1>')
    return redirect('/admin/xero/gfsaxeroitemcode')


def get_contacts_dict(contacts):
    xero_dict = {}
    if type(contacts) == list:
        for contact in contacts:
            xero_dict[contact['Name']] = contact
    elif type(contacts) == dict:
        xero_dict[contacts['Name']] = contacts
    return xero_dict

def compare_contact(request):
    members_difference = ""
    xero = access_to_xero(request)
    try:
        xero_contacts = xero.contacts.all()
    except:
        traceback.print_exe()
        return HttpResponse('<h1>Failed to get XERO contacts</hi>')
    xero_contacts_dict = get_contacts_dict(xero_contacts)
    gfsa_contacts = GFSAXeroContactPerson.objects.all()
    for gfsa_contact in gfsa_contacts:
        if gfsa_contact.in_xero == False:
            continue
        if gfsa_contact.contact_name != None:
            #print ("Name: %s, FN: %s, LN: %s, Email: %s" %(gfsa_contact.contact_name, gfsa_contact.first_name, gfsa_contact.last_name, gfsa_contact.email_address))
            try:
                xero_contact = xero_contacts_dict[gfsa_contact.contact_name]
            except:
                xero_contact = None
            if xero_contact != None:
                #print ("Name: %s, FN: %s, LN: %s, Email: %s" %(gfsa_contact.contact_name, xero_contact['FirstName'], xero_contact['LastName'], xero_contact['EmailAddress']))
                if gfsa_contact.first_name.lower() != xero_contact['FirstName'].lower() or\
                gfsa_contact.last_name.lower() != xero_contact['LastName'].lower() or\
                gfsa_contact.email_address.lower() != xero_contact['EmailAddress'].lower() or\
                gfsa_contact.phone.lower() != get_mobile_no(xero_contact['Phones']).lower():
                    members_difference += "\nModified:"
                    members_difference += "\n" + " ".join([
                        "GFSA: "+ gfsa_contact.first_name.lower(),
                        gfsa_contact.last_name.lower(),
                        gfsa_contact.email_address.lower(),
                        gfsa_contact.phone.lower()])
                    members_difference += "\n" + " ".join([
                        "XERO:",
                        xero_contact['FirstName'].lower(),
                        xero_contact['LastName'].lower(),
                        xero_contact['EmailAddress'].lower(),
                        get_mobile_no(xero_contact['Phones']).lower()])
        else: #else the contact has not yet been added to xero or need to be synched with xero
            #print ("Name: %s, FN: %s, LN: %s, Email: %s" %(gfsa_contact.contact_name, gfsa_contact.first_name, gfsa_contact.last_name, gfsa_contact.email_address))
            for key in xero_contacts_dict:
                xero_contact = xero_contacts_dict[key]
                if xero_contact['FirstName'].lower() == gfsa_contact.first_name.lower() and\
                   xero_contact['LastName'].lower() == gfsa_contact.last_name.lower():
                    gfsa_contact.contact_name = xero_contact['Name']
                    gfsa_contact.save()
            if gfsa_contact.contact_name == None:
                members_difference += "\nAdded:"
                members_difference += "\n" + " ".join([
                    "GFSA: "+ gfsa_contact.first_name.lower(),
                    gfsa_contact.last_name.lower(),
                    gfsa_contact.email_address.lower(),
                    gfsa_contact.phone.lower()])
    print members_difference
    if len(members_difference)>0:       
        email_admin(members_difference)
    return redirect('/admin')


def get_item_line(itemcode, quantity, discountRate, description):
    item_line = {}

    item_line['ItemCode'] = itemcode
    item_line['Quantity'] = quantity
    item_line['DiscountRate'] = discountRate
    item_line['Description'] = description

    return item_line


def get_contact_name(name):
    contact = {}
    contact['Name'] = name
    return contact


def get_invoice(inv_type, contact, line_items):
    invoice = {}

    invoice['Type'] = inv_type
    invoice['Contact'] = contact
    invoice['Status'] = 'DRAFT'
    invoice['LineItems'] = line_items

    return invoice


def upload(request, invoice):
    xero = access_to_xero(request)

    try:
        xero.invoices.put(invoice)

    except:
        return False

    return True

def get_mobile_no(phones):

    mobile_no = ''
    valid = False
    
    for phone in phones:
        
        for key in phone:

            if key == 'PhoneType':
                if phone[key] == 'MOBILE':
                    valid = True

            if key == 'PhoneCountryCode':
                mobile_no = '+' + phone[key] + mobile_no

            if key == 'PhoneAreaCode':
                mobile_no += phone[key]

            if key == 'PhoneNumber':
                mobile_no = mobile_no + phone[key]
            
    if valid:
        print mobile_no
        return mobile_no
    else:
        return ''

def send_notification(request):

    flight_records_set = GfsaFlightRecords.objects.filter(fr_sent = False, fr_tug_duration__isnull = False, fr_glider_duration__isnull = False)

    if flight_records_set.exists():

        for flight_record in flight_records_set:

            send_sms_p1 = False
            send_sms_p2 = False
            send_email_p1 = False
            send_email_p2 = False
            
            tug_duration = int(flight_record.fr_tug_duration)/60.0
            glider_duration = int(flight_record.fr_glider_duration)/60.0
            p1 = str(flight_record.fr_p1_id)
            p2 = str(flight_record.fr_p2_id)
            p1_pay_percent = int(flight_record.fr_p1_pay_percent)
            p2_pay_percent = int(flight_record.fr_p2_pay_percent)

            notification = p1 + ' pays ' + str(p1_pay_percent) + '% ' + p2 + ' pays ' + str(p2_pay_percent) + '% ' + \
                ' Tug Duration: ' + str(tug_duration) + ' Glider Duration: ' +\
                str(glider_duration) + ' Comment: ' + str(flight_record.fr_comment)

            try:
                member_p1 = GFSAXeroContactPerson.objects.get(contact_name=p1)
                send_email_p1 = True
                p1_mobile = member_p1.phone

                if p1_mobile is not None:
                    send_sms_p1 = True
                
            except:
                pass

            try:
                member_p2 = GFSAXeroContactPerson.objects.get(contact_name=p2)
                send_email_p2 = True
                p2_mobile = member_p2.phone

                if p2_mobile is not None:
                    send_sms_p2 = True
                
            except:
                pass

            if send_email_p1:
            
                if email_anyone(member_p1.email_address, notification):
                    flight_record.fr_sent = True

            if send_email_p2:

                if email_anyone(member_p2.email_address, notification):
                    flight_record.fr_sent = True

            if send_sms_p1:
                print "PPPPPPPPPPPP1111"
                if send_SMS(p1_mobile, notification):
                    flight_record.fr_sent = True

            if send_sms_p2:
                print "PPPPPPPPPPPP22222222"
                if send_SMS(p2_mobile, notification):
                    flight_record.fr_sent = True

            flight_record.save()

    return redirect('/admin')
