#include <iostream>
#include <windows.h>
#include <string>
#include <thread>
#include <chrono>
#include <fstream>
#include <regex>
#include <unordered_map>

// Function to decode HTML entities
std::string decodeHtmlEntities(const std::string& input) {
    std::unordered_map<std::string, char> htmlEntities = {
        {"&gt;", '>'},
        {"&lt;", '<'},
        {"&amp;", '&'},
        {"&quot;", '"'},
        {"&apos;", '\''}
    };

    std::string result;
    size_t pos = 0;
    while (pos < input.size()) {
        if (input[pos] == '&') {
            size_t semicolonPos = input.find(';', pos);
            if (semicolonPos != std::string::npos) {
                std::string entity = input.substr(pos, semicolonPos - pos + 1);
                auto it = htmlEntities.find(entity);
                if (it != htmlEntities.end()) {
                    result.push_back(it->second);
                    pos = semicolonPos + 1;
                }
                else {
                    result.push_back(input[pos]);
                    pos++;
                }
            }
            else {
                result.push_back(input[pos]);
                pos++;
            }
        }
        else {
            result.push_back(input[pos]);
            pos++;
        }
    }
    return result;
}

// Function to extract the RID number from the URL
std::string extractRID(const std::string& url) {
    std::regex ridRegex(R"(rid=(\d+))");
    std::smatch match;
    if (std::regex_search(url, match, ridRegex)) {
        return match[1].str();
    }
    return "unknown";
}

int main() {
    std::string chromePath = R"(C:\Program Files\Google\Chrome\Application\chrome.exe)";
    std::string url = "https://aad.archives.gov/aad/record-detail.jsp?dt=178&mtch=52242&cat=all&sc=5746,5778,5749,5757,5761,5762,5763,5777,5767&cl_5749=E%2CD%2CA%2CF%2CB%2CC%2CG&op_5749=null&nfo_5749=V,1,1900&cl_5757=AD%2CAB%2CAR%2CFA%2CAV%2CCV%2CCS%2CEN%2CIN%2CMI%2CMD%2CMP%2COD%2CTC&op_5757=null&nfo_5757=V,2,1900&mtch=52242&bc=,sl,fd&rpp=10&pg=31&tf=F&rid=33068&rlst=17939,32686,33068,33069,61342,61343,61350,61352,61359,61363";

    while (true) {
        // Extract the RID number from the URL
        std::string rid = extractRID(url);
        std::string outputFile = "equip_html_" + rid + ".txt";

        std::string command = chromePath + " --headless --incognito --dump-dom --virtual-time-budget=60000 --disable-gpu --no-sandbox --window-size=1280x1024 --disable-software-rasterizer --disable-extensions --remote-debugging-port=9222 --disable-dev-shm-usage " + url;

        STARTUPINFOA si = { sizeof(STARTUPINFOA) };
        PROCESS_INFORMATION pi;
        SECURITY_ATTRIBUTES sa;
        sa.nLength = sizeof(sa);
        sa.lpSecurityDescriptor = NULL;
        sa.bInheritHandle = TRUE;

        HANDLE hFile = CreateFileA(outputFile.c_str(), GENERIC_WRITE, 0, &sa, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
        if (hFile == INVALID_HANDLE_VALUE) {
            std::cerr << "Error: Unable to create output file!" << std::endl;
            return 1;
        }

        si.dwFlags = STARTF_USESTDHANDLES;
        si.hStdOutput = hFile;
        si.hStdError = hFile;

        if (!CreateProcessA(NULL, &command[0], NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)) {
            std::cerr << "Error: Could not create process. " << GetLastError() << std::endl;
            CloseHandle(hFile);
            return 1;
        }

        std::this_thread::sleep_for(std::chrono::seconds(5));
        TerminateProcess(pi.hProcess, 0);
        WaitForSingleObject(pi.hProcess, INFINITE);

        // Properly close and release the file handle
        FlushFileBuffers(hFile);
        CloseHandle(hFile);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));

        // Clean up process handles
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);

        std::ifstream file(outputFile);
        if (!file.is_open()) {
            std::cerr << "Error: Could not open the file " << outputFile << std::endl;
            return 1;
        }

        std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
        file.close();

        std::regex hrefRegex(R"(<a\s+href=\"([^\"]+)\"[^>]*>Next Record\s*&gt;</a>)");
        std::smatch match;

        if (std::regex_search(content, match, hrefRegex)) {
            std::string rawUrl = match[1].str();
            url = "https://aad.archives.gov/aad/" + decodeHtmlEntities(rawUrl);
            std::cout << "Next URL: " << url << std::endl;
        }
        else {
            std::cerr << "No URL found for 'Next Record' in the HTML content. Stopping." << std::endl;
            break;
        }
    }

    return 0;
}
