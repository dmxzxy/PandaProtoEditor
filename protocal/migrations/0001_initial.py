# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-08 04:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('fullname', models.CharField(max_length=150)),
                ('desc', models.CharField(max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnumValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('fullname', models.CharField(max_length=150)),
                ('desc', models.CharField(max_length=150)),
                ('number', models.IntegerField()),
                ('enum', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='protocal.Enum')),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('fullname', models.CharField(max_length=150)),
                ('desc', models.CharField(max_length=150)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FieldLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='FieldType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField()),
                ('typename', models.CharField(max_length=150)),
                ('desc', models.CharField(max_length=150)),
                ('priority', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Lock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lock_owner', models.CharField(max_length=150)),
                ('lock_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('fullname', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('fullname', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('namespace', models.CharField(max_length=150, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectBranche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('proto_url', models.CharField(max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protocal.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Protocal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocal_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protocal.Message')),
            ],
        ),
        migrations.CreateModel(
            name='ProtocalLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='protocal',
            name='protocal_label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protocal.ProtocalLabel'),
        ),
        migrations.AddField(
            model_name='protocal',
            name='protocal_ref',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='protocal.Protocal'),
        ),
        migrations.AddField(
            model_name='module',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protocal.ProjectBranche'),
        ),
        migrations.AddField(
            model_name='message',
            name='module',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='protocal.Module'),
        ),
        migrations.AddField(
            model_name='message',
            name='nested',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='protocal.Message'),
        ),
        migrations.AddField(
            model_name='fieldtype',
            name='project',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='protocal.ProjectBranche'),
        ),
        migrations.AddField(
            model_name='field',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protocal.FieldLabel'),
        ),
        migrations.AddField(
            model_name='field',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protocal.Message'),
        ),
        migrations.AddField(
            model_name='field',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protocal.FieldType'),
        ),
        migrations.AddField(
            model_name='enum',
            name='module',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='protocal.Module'),
        ),
        migrations.AddField(
            model_name='enum',
            name='nested',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='protocal.Message'),
        ),
    ]
