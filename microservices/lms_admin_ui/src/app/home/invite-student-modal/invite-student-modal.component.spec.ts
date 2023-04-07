import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InviteStudentModalComponent } from './invite-student-modal.component';

describe('InviteStudentModalComponent', () => {
  let component: InviteStudentModalComponent;
  let fixture: ComponentFixture<InviteStudentModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InviteStudentModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InviteStudentModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
