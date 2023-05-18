import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ToolFormComponent } from './tool-form.component';

describe('ToolFormComponent', () => {
  let component: ToolFormComponent;
  let fixture: ComponentFixture<ToolFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ToolFormComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ToolFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
