from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponseRedirect
from .forms import MediaFileForm
from .models import MediaFile
import os
from django.conf import settings
from django.contrib import messages
from django.urls import reverse

def media_management(request):
    files = MediaFile.objects.all().order_by('-date_uploaded')
    form = MediaFileForm()

    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        files_to_upload = request.FILES.getlist('file')
        successfully_uploaded = 0  # Counter for successful uploads
        error_occurred = False

        if len(files_to_upload) > 10:
            messages.error(request, "You cannot upload more than 10 files at a time.")
            error_occurred = True
        else:
            for uploaded_file in files_to_upload:
                # Validate each file manually through the form
                form = MediaFileForm({'file': uploaded_file}, {'file': uploaded_file})  # Recreate form for each file
                if form.is_valid():
                    file_type = uploaded_file.content_type.split('/')[0]
                    category = 'Image' if file_type == 'image' else 'Audio' if file_type == 'audio' else 'Video'

                    MediaFile.objects.create(
                        file=uploaded_file,
                        file_name=uploaded_file.name,
                        size=uploaded_file.size,
                        file_type=file_type,
                        category=category
                    )
                    successfully_uploaded += 1
                else:
                    error_occurred = True
                    for error in form.errors.get('file', []):
                        messages.error(request, f"{uploaded_file.name}: {error}")

        if successfully_uploaded > 0 and not error_occurred:
            messages.success(request, f"{successfully_uploaded} file(s) uploaded successfully!")
            return HttpResponseRedirect(reverse('upload_files'))  # Redirect to clear form and show updates

    # Clear messages to prevent duplication on page refresh
    storage = messages.get_messages(request)
    storage.used = True

    return render(request, 'upload.html', {'files': files, 'form': form})


def download_file(request, file_id):
    media_file = MediaFile.objects.get(id=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, media_file.file.name)
    return FileResponse(open(file_path, 'rb'), as_attachment=True)

def delete_file(request, file_id):
    media_file = MediaFile.objects.get(id=file_id)
    media_file.file.delete()
    media_file.delete()
    messages.error(request, "File deleted successfully.")
    return redirect('upload_files')
