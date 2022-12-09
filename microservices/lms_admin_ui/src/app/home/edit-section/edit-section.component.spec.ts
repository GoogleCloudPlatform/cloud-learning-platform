import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditSectionComponent } from './edit-section.component';

describe('EditSectionComponent', () => {
  let component: EditSectionComponent;
  let fixture: ComponentFixture<EditSectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EditSectionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EditSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
