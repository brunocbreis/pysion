{ 
    Tools = { 
        Square = MacroOperator { 
            Inputs = { 
                CoolWidth = InstanceInput { 
                    Name = "Cool Width", 
                    SourceOp = "Rect", 
                    Source = "Width", 
                    Default = 0.6, 
                }, 
            }, 
            Outputs =  { 
                Output = InstanceOutput { 
                    SourceOp = "Render", 
                    Source = "Output", 
                },  
            }, 
            Tools = { 
                Rect = sRectangle { 
                    Inputs =  { 
                        Red = Input { Value = 0.2, }, 
                        Green = Input { Value = 0.3, }, 
                        Blue = Input { Value = 0.4, }, 
                        Alpha = Input { Value = 1, }, 
                        Width = Input { Value = 0.6, }, 
                        Height = Input { 
                            Value = 0.3, 
                            Expression = "Width / 2", 
                        }, 
                    }, 
                    ViewInfo = OperatorInfo { Pos = { 0, 0 }, }, 
                }, 
                Render = sRender { 
                    Inputs =  { 
                        Input = Input { 
                            SourceOp = "Rect", 
                            Source = "Output", 
                        }, 
                        Width = Input { Value = 1920, }, 
                        Height = Input { Value = 1080, }, 
                    }, 
                    ViewInfo = OperatorInfo { Pos = { 110, 0 }, }, 
                }, 
            }, 
            ViewInfo = OperatorInfo { Pos = { 0, 0 }, }, 
        }, 
    }, 
    ActiveTool = "Square" 
}