import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { LmsJobsListComponent } from './lms-jobs-list.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('LmsJobsListComponent', () => {
  let component: LmsJobsListComponent;
  let fixture: ComponentFixture<LmsJobsListComponent>;
  let dialogRef
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports : [MatLegacyDialogModule, HttpClientTestingModule],
      declarations: [ LmsJobsListComponent ],
      providers: [ MatDialog, MatDialogRef]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LmsJobsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
