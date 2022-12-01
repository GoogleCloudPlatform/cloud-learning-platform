import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CourseTemplateComponent } from './course-template.component';

describe('CourseTemplateComponent', () => {
  let component: CourseTemplateComponent;
  let fixture: ComponentFixture<CourseTemplateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CourseTemplateComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CourseTemplateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
