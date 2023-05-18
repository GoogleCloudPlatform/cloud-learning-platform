import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ToolsListComponent } from './tools-list.component';

describe('ToolsListComponent', () => {
  let component: ToolsListComponent;
  let fixture: ComponentFixture<ToolsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ToolsListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ToolsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
