import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { CreateAssignmentComponent } from './create-assignment.component';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { FormBuilder } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { AngularFireModule } from '@angular/fire/compat';
import { environment } from 'src/environments/environment';

describe('CreateAssignmentComponent', () => {
  let component: CreateAssignmentComponent;
  let fixture: ComponentFixture<CreateAssignmentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ MatLegacyDialogModule, HttpClientTestingModule,
      AngularFireModule.initializeApp(environment.firebase)],
      declarations: [ CreateAssignmentComponent ],
      providers: [MatSnackBar, FormBuilder,
        {provide:MatDialogRef, useValue: jasmine.createSpyObj('MatDialogRef', ['close', 'disableClose'])},
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Create', init_data: '', extra_data:{} }}

      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateAssignmentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
