import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateCourseTemplateModalComponent } from './create-course-template-modal.component';

describe('CreateCourseTemplateModalComponent', () => {
  let component: CreateCourseTemplateModalComponent;
  let fixture: ComponentFixture<CreateCourseTemplateModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreateCourseTemplateModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateCourseTemplateModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
