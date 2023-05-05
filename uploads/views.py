from django.shortcuts import render, redirect, get_object_or_404

from .utils import *

from .decorators import *
from .models import *
from .forms import *

from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required

import numpy as np

from django.urls import reverse

# from django.http import Http404

# from django.shortcuts import (
# render_to_response
# )

# from django.template import RequestContext


# Create your views here.
def index(request):
    authenticate = request.user.is_authenticated
    return render(request, 'index.html' , {'authenticate':authenticate})


def service(request):
    authenticate = request.user.is_authenticated
    context = {'authenticate':authenticate}
    return  render(request, 'service.html',context)


def about(request):
    authenticate = request.user.is_authenticated
    context = {'authenticate':authenticate}
    return  render(request, 'about.html',context)


@login_required(login_url='signin')
def prediction(request):
    authenticate = request.user.is_authenticated
    return render(request, 'prediction.html' ,{'uploaded':True,'file_url':True, 'authenticate':authenticate})

def contact(request):
    authenticate = request.user.is_authenticated
    context = {'authenticate':authenticate}
    return  render(request, 'contact.html',context)


def after_proccess(request):
    authenticate = request.user.is_authenticated
    
    # Getting last uploaded image
    image = upload.objects.last()


    # Removing Background
    #print("Removing Image background") 
    removed_bg = Removed_bg_Image(image.image)
    #print("Removed Image background")
    #Reading RGB Image 

    Orig_image = cv2.imread(f'media/{image.image}') 
    print(Orig_image.shape) 

    rgb_image = Read_Image(removed_bg) 
      
    rgb_original_image = Read_Image(Orig_image)     

    # Converting to gray
    gray_image = Gray_Scale_Image(rgb_image)

    # Converting to equalized
    eq_hist = Equalized_Hist(gray_image)

    # Plotting histograms
    hist, bins = np.histogram(gray_image.ravel(), 256, [0, 256])
    equ_hist, equ_bins = np.histogram(eq_hist.ravel(), 256, [0, 256])

    # plt.hist(gray_image.flatten(), bins=255, range=(0,255))
    # eq_fig = plt.hist(eq_hist.ravel(), bins=256, color='r', alpha=0.5)
    # plt.savefig(f'media/GrayScale_Histogram/{image.image}')
    # eq_fig.savefig(f'media/Equalized_Histogram/{image.image}')

    # Converting to Binary
    binary_image = Binary_Image(gray_image)
    #print("Binary Image done") 

    # Converting to Morphology
    Morph_image = Morphology_Image(binary_image)
    #print("Morphological Image done") 

    # Figuring out number of infected region
    Contour, leaf_Area, infected_area, Number_of_contour   = Contours(binary_image)
    #print("Contours done") 
    #print("Total Contours",len(Contour))

    # Drawing image of number of infected region
    spot_on_org_img, black_img = Contours_On_Orinial(rgb_image, Contour)
    
    # Saving Images 
    Save_Images(image.image,rgb_original_image, rgb_image, gray_image, eq_hist, binary_image, Morph_image, spot_on_org_img, black_img)

    # infected = upload.objects.create(InfectedRegion=spot_on_org_img)
    # infected.save()

    # Mathematical calculation to convert the area of pixels into cm^2
    leaf_Area = round(0.0624583333*leaf_Area,3)
    infected_area = round(0.0624583333*infected_area,3)
    #print("Model renders")  
    

    # Mathematical calculation to find the ratio
    Ratio = round(infected_area/leaf_Area,2)*100

    # Indicating the level by number of spots
    if Number_of_contour >= 98:
        Severe = "Severe"
    elif Number_of_contour <= 98 and Number_of_contour >= 50:
        Severe = "Moderate"
    else:
        Severe = "Low"
    
    found_disease, data = predict(image.image)
    #print("type ",type(found_disease))
    treatment = Treatment.objects.get(disease=found_disease)
    symptoms, caused, organic_control, chemical_control, preventive_measures = get_treatment(treatment)
    
    #print("Hurrah! Successfully done")

    Disease_classification = data
    context = { 'preprocess_url':image.image , 'leaf_Area': leaf_Area , 'Num_of_contour':Number_of_contour,
                'infected_area':infected_area , 'Ratio':Ratio, 'Severe':Severe , 'uploaded':False,
                'found_disease':found_disease,'authenticate':authenticate,
                'symptoms':symptoms , 'caused':caused , 'organic_control':organic_control,'chemical_control':chemical_control,
                'preventive_measures':preventive_measures,"Disease_classification" : Disease_classification,
                'hist': hist.tolist(),
                'bins': bins.tolist(),
                'equ_hist': equ_hist.tolist(),
                'equ_bins': equ_bins.tolist(),}
    return  render(request, 'prediction.html', context)


@login_required(login_url='signin')
def uploaded(request):
    error = ""
    errorfound_or_not = False
    authenticate = request.user.is_authenticated
    if 'original_image' not in request.FILES:
        # If 'original_image' key is not found, return the prediction template
        context = {'uploaded':True ,'login':True , 'file_url':True,'authenticate':authenticate}
        return render(request, 'prediction.html', context)

    try:
        #print("uploading..........")
        uploaded = request.FILES['original_image']
        upl = upload.objects.create(image=uploaded)
        upl.save()
        #print("Successfully uploaded Image")
        return after_proccess(request)
    except AttributeError:
        errorfound_or_not = True
        #print("Invalid input: file object expected")
        error = "Invalid input: file object expected"
    except TypeError:
        errorfound_or_not = True
        #print("Invalid input: file type not supported")
        error = "Invalid input: file type not supported"
    except Exception as e:
        if str(e) == 'original_image':
            # No error message needed if 'original_image' is in exception message
            pass
        else:
            errorfound_or_not = True
            print("Error occurred: ", e)
            error = "Please Enter the Correct Image Format."

    context = {'uploaded':True ,'login':True , 'file_url':True,'authenticate':authenticate,
               'errorfound' : error , 'errorfound_or_not':errorfound_or_not}
    return render(request, 'prediction.html', context)

def logout_Page(request):
    logout(request)
    return redirect('home')

@login_required(login_url='signin')
def user(request):
    profile_setting = True
    success_updated = False
    error = False
    
    authenticate = request.user.is_authenticated
    user = get_object_or_404(User,  pk=request.user.pk)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            success_updated = True
            print("updated")
            messages.success(request, 'Your profile is updated successfully')

            return redirect('user') 
        else:
            error=True
        
    else:
        print("updatadssadsed")
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'user_profile.html', {
        'user_form': user_form,
        'authenticate': authenticate,
        'error': error,
        'user': user,
        'profile_setting': profile_setting,
    })


@login_required(login_url='signin')
def change_pass(request):
    authenticate = request.user.is_authenticated

    change_passw = True
    success_updated = False
    form = PasswordChangeForm(user=request.user, data=request.POST)
    error_message = ''  # Initialize error_message to an empty string

    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        success_updated = True
        # messages.success(request, 'Your password was successfully updated!')
        # Add success message to template context
        success_message = 'Your password was successfully updated!'
    else:
        # messages.error(request, 'Please correct the error below.')
        error_message = " ".join([error[0] for error in form.errors.values()])
        # Add error message to template context
        success_message = ''

    # Filter out empty form fields
    
        
    return render(request, 'user_profile.html', {'form': form, 'error_message': error_message, 
                                                 'change_passw': change_passw,
                                                 'success_updated':success_updated,
                                                 'success_message': success_message,
                                                 'authenticate':authenticate})


# HTTP Error 400
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)


def disease_details(request, disease):
    # Get the Treatment object associated with the provided disease name
    # try:
    treatment = Treatment.objects.get(disease=disease)
    # except Treatment.DoesNotExist:
    #     # If no Treatment object exists for this disease, return a 404 error
    #     raise Http404("No treatment found for this disease.")
    
    # Get the treatment details
    symptoms, caused, organic_control, chemical_control, preventive_measures = get_treatment(treatment)
    # Pass the details to the template in a context dictionary
    context = {
        'treatment': treatment,
        'symptoms': symptoms,
        'caused': caused,
        'organic_control': organic_control,
        'chemical_control': chemical_control,
        'preventive_measures': preventive_measures,
    }

    return render(request, 'disease_details.html', context)


@unauthenticated_user
def signin(request):
    error_login = False
    form = CreateUserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                # redirect to admin site if user is an admin
                login(request, user)
                return redirect(reverse('admin:index'))
            else:
                login(request, user)
                # redirect to home page if user is not an admin
                return redirect('home')
        else:
            error_login = True
            messages.error(request, 'Username or password is incorrect')

    context = {'signin': True, 'form':form,'error_login':error_login}
    return render(request, 'login_signup.html', context)

@unauthenticated_user
def signup(request):
    form = CreateUserForm()
    error_signup = False
    
    if request.method == 'POST': 
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print('asmdnasd')
            user = form.save()
            form.cleaned_data.get('email')
            form.cleaned_data.get('username')
            form.cleaned_data.get('password1')
            form.cleaned_data.get('password2')
            group = Group.objects.get(name='user')
            user.groups.add(group)
            form = CreateUserForm()  # Instantiate new form on success
            login(request, user)
            return redirect('home')
        else:
            # Add validation errors to the form
            error_signup = True
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")


    context = {'signup': True, 'form': form, 'error_signup': error_signup}

    return render(request, 'login_signup.html', context)