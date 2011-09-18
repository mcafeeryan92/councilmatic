# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Opinion'
        db.create_table('opinions_opinion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('opiner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='opinions', to=orm['auth.User'])),
        ))
        db.send_create_signal('opinions', ['Opinion'])

        # Adding M2M table for field agreers on 'Opinion'
        db.create_table('opinions_opinion_agreers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('opinion', models.ForeignKey(orm['opinions.opinion'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('opinions_opinion_agreers', ['opinion_id', 'user_id'])

        # Adding model 'StatementRevision'
        db.create_table('opinions_statementrevision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('opinion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', to=orm['opinions.Opinion'])),
            ('statement', self.gf('django.db.models.fields.TextField')()),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('opinions', ['StatementRevision'])


    def backwards(self, orm):
        
        # Deleting model 'Opinion'
        db.delete_table('opinions_opinion')

        # Removing M2M table for field agreers on 'Opinion'
        db.delete_table('opinions_opinion_agreers')

        # Deleting model 'StatementRevision'
        db.delete_table('opinions_statementrevision')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'opinions.opinion': {
            'Meta': {'object_name': 'Opinion'},
            'agreers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'agreements'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opiner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'opinions'", 'to': "orm['auth.User']"})
        },
        'opinions.statementrevision': {
            'Meta': {'object_name': 'StatementRevision'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opinion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'to': "orm['opinions.Opinion']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'statement': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['opinions']
