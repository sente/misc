diveline.connect("localhost", "di_xxxxxx", "xxxx");


model.open(model,"/sales/sales_MA.mdl");
dive (model, "Distributor"){
	walk (model, "Distributor"){
		dive (model, "Account"){
			walk (model, "Account"){
				console.writeln (Dimension["Distributor"] + " " +  Dimension["Account"]);
			}
		}
	}
}

diveline.disconnect();
