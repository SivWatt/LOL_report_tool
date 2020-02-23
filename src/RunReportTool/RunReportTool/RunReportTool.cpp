// RunReportTool.cpp : 此檔案包含 'main' 函式。程式會於該處開始執行及結束執行。
//

//#include "pch.h"
#include <iostream>
#include <filesystem>
#include <sstream>

using namespace std;
namespace fs = filesystem;

int main(int argc, const char * argv[])
{
	fs::path currPath = fs::current_path();
	wstring wstrCmd = L"start /b pythonw ";

	wstrCmd += currPath.wstring();
	wstrCmd += L"\\League.py";

	_wsystem( wstrCmd.c_str() );

	return 0;
}
