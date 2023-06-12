import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LmsJobsListComponent } from './lms-jobs-list.component';

describe('LmsJobsListComponent', () => {
  let component: LmsJobsListComponent;
  let fixture: ComponentFixture<LmsJobsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LmsJobsListComponent ]
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
