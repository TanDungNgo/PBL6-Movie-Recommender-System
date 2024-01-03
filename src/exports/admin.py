from django.contrib import admin

# Register your models here.
from .models import Export, ExportModelNCF
class ExportAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'timestamp', 'latest']
    list_filter = ['type', 'timestamp', 'latest']
    search_fields = ['type', 'timestamp', 'latest']
    readonly_fields = ['id', 'timestamp']
    class Meta:
        model = Export
class ExportModelNCFAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'n_epochs', 'batch_size', 'learning_rate', 'embedding_size', 'timestamp']
    list_filter = ['n_epochs', 'batch_size', 'learning_rate', 'embedding_size', 'timestamp']
    search_fields = ['n_epochs', 'batch_size', 'learning_rate', 'embedding_size', 'timestamp']
    readonly_fields = ['id', 'timestamp']
    class Meta:
        model = ExportModelNCF

admin.site.register(Export, ExportAdmin)
admin.site.register(ExportModelNCF, ExportModelNCFAdmin)