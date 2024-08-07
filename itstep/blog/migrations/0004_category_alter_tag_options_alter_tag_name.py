# Generated by Django 5.0.7 on 2024-08-06 14:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_tag_alter_post_publish_post_tags"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(default="", max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={"verbose_name": "tags for posts"},
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(
                help_text="A label for name tag.", max_length=31, unique=True
            ),
        ),
    ]
